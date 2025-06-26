from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import User, Contact, UserProfile

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Z][a-z]*$',
                message='First name must start with a capital letter followed by lowercase letters'
            )
        ]
    )
    last_name = forms.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r'^[A-Z][a-z]*$',
                message='Last name must start with a capital letter followed by lowercase letters'
            )
        ]
    )
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message='Phone number must be in format: +7XXXXXXXXXX'
            )
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        return user

class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Z][a-z]*$',
                message='Name must start with a capital letter followed by lowercase letters'
            )
        ]
    )

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'interests', 'avatar', 'preferred_language']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'interests': forms.Textarea(attrs={'rows': 3}),
        } 