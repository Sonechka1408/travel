from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'destination_id', 'user_id', 'text', 'created_at']
        read_only_fields = ['user_id'] 