from django.db import models

class Like(models.Model):
    user_id = models.IntegerField()
    destination_id = models.IntegerField(null=True, blank=True)
    comment_id = models.IntegerField(null=True, blank=True)
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [
            ('user_id', 'destination_id'),
            ('user_id', 'comment_id'),
        ]

    def __str__(self):
        target = f"destination {self.destination_id}" if self.destination_id else f"comment {self.comment_id}"
        action = "likes" if self.is_like else "dislikes"
        return f"User {self.user_id} {action} {target}" 