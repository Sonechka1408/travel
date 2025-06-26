from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
import json
import requests

from .models import Destination, Contact, User, UserProfile, Comment, Like
from .forms import UserRegistrationForm, ContactForm, UserProfileForm

def home(request):
    destinations = Destination.objects.all()[:3]
    return render(request, 'portal/index.html', {'destinations': destinations})

def about(request):
    return render(request, 'portal/about.html')

class DestinationListView(ListView):
    model = Destination
    template_name = 'portal/destinations.html'
    context_object_name = 'destinations'

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'portal/destination_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_like'] = Like.objects.filter(
                user=self.request.user,
                destination=self.object
            ).first()
        return context

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to Travel Portal.')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    return render(request, 'portal/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    return render(request, 'portal/profile.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            if request.user.is_authenticated:
                contact.user = request.user
            contact.save()
            
            # Send message to Telegram
            if settings.TELEGRAM_BOT_TOKEN and settings.TELEGRAM_CHAT_ID:
                message = f"""
New Contact Form Message:
Name: {contact.name}
Email: {contact.email}
Subject: {contact.subject}
Message: {contact.message}
                """
                
                try:
                    response = requests.post(
                        f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage',
                        json={
                            'chat_id': settings.TELEGRAM_CHAT_ID,
                            'text': message,
                            'parse_mode': 'HTML'
                        }
                    )
                    response.raise_for_status()
                except requests.RequestException as e:
                    messages.error(request, 'Failed to send notification to admin.')
                else:
                    messages.success(request, 'Message sent successfully!')
            
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'portal/contact.html', {'form': form})

@login_required
@require_POST
def create_comment(request):
    try:
        data = json.loads(request.body)
        destination = get_object_or_404(Destination, id=data.get('destination_id'))
        text = data.get('text')

        if not text:
            raise ValidationError('Comment text is required')

        comment = Comment.objects.create(
            destination=destination,
            user=request.user,
            text=text
        )

        return JsonResponse({
            'status': 'success',
            'comment': comment.to_json()
        })
    except (ValidationError, ValueError) as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def get_comments(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    comments = destination.comments.all()
    return JsonResponse({
        'status': 'success',
        'comments': [comment.to_json() for comment in comments]
    })

@login_required
@require_POST
def handle_like(request):
    try:
        data = json.loads(request.body)
        destination_id = data.get('destination_id')
        comment_id = data.get('comment_id')
        action = data.get('action')

        if action not in ['like', 'dislike']:
            raise ValidationError('Invalid action')

        if destination_id:
            target = get_object_or_404(Destination, id=destination_id)
            like, created = Like.objects.get_or_create(
                user=request.user,
                destination=target,
                defaults={'is_like': action == 'like'}
            )
        elif comment_id:
            target = get_object_or_404(Comment, id=comment_id)
            like, created = Like.objects.get_or_create(
                user=request.user,
                comment=target,
                defaults={'is_like': action == 'like'}
            )
        else:
            raise ValidationError('No target specified')

        if not created:
            if like.is_like == (action == 'like'):
                like.delete()
                user_action = None
            else:
                like.is_like = action == 'like'
                like.save()
                user_action = action
        else:
            user_action = action

        response_data = {
            'status': 'success',
            'user_action': user_action,
        }

        if destination_id:
            response_data.update({
                'likes': target.get_likes_count(),
                'dislikes': target.get_dislikes_count()
            })
        else:
            response_data.update({
                'likes': target.like_set.filter(is_like=True).count(),
                'dislikes': target.like_set.filter(is_like=False).count()
            })

        return JsonResponse(response_data)
    except (ValidationError, ValueError) as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def delete_comment(request):
    try:
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        
        if not comment_id:
            raise ValidationError('Comment ID is required')
            
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Comment deleted successfully'
        })
    except (ValidationError, ValueError) as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400) 