from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        destination_id = self.request.query_params.get('destination_id', None)
        if destination_id is not None:
            return Comment.objects.filter(destination_id=destination_id)
        return Comment.objects.all()

    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAdminUser])
    def delete(self, request, pk=None):
        comment = self.get_object()
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 