from rest_framework import serializers
from .models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = ['id', 'name', 'description', 'image', 'created_at', 'likes_count', 'dislikes_count']

    def get_likes_count(self, obj):
        return obj.get_likes_count()

    def get_dislikes_count(self, obj):
        return obj.get_dislikes_count() 