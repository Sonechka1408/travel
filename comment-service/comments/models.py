from django.db import models

class Comment(models.Model):
    destination_id = models.IntegerField()
    user_id = models.IntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by user {self.user_id} on destination {self.destination_id}"

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        } 