from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_likes_count(self):
        return self.likes.filter(is_like=True).count()

    def get_dislikes_count(self):
        return self.likes.filter(is_like=False).count() 