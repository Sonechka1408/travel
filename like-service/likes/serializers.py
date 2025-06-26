from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user_id', 'destination_id', 'comment_id', 'is_like', 'created_at']
        read_only_fields = ['user_id'] 