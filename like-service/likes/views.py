from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Like
from .serializers import LikeSerializer

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        destination_id = request.data.get('destination_id')
        comment_id = request.data.get('comment_id')
        action = request.data.get('action')

        if action not in ['like', 'dislike']:
            return Response(
                {'error': 'Invalid action'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not destination_id and not comment_id:
            return Response(
                {'error': 'No target specified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        filter_kwargs = {
            'user_id': request.user.id,
            'destination_id' if destination_id else 'comment_id': destination_id or comment_id
        }

        like, created = Like.objects.get_or_create(
            **filter_kwargs,
            defaults={'is_like': action == 'like'}
        )

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

        target_likes = Like.objects.filter(
            Q(destination_id=destination_id) if destination_id else Q(comment_id=comment_id)
        )

        return Response({
            'status': 'success',
            'user_action': user_action,
            'likes': target_likes.filter(is_like=True).count(),
            'dislikes': target_likes.filter(is_like=False).count()
        }) 