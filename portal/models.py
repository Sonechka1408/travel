from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+7\d{10}$',
                message='Phone number must be in format: +7XXXXXXXXXX'
            )
        ],
        unique=True,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def get_likes_count(self):
        return self.like_set.filter(is_like=True).count()

    def get_dislikes_count(self):
        return self.like_set.filter(is_like=False).count()

class Comment(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username} on {self.destination.name}"

    def to_json(self):
        return {
            'id': self.id,
            'text': self.text,
            'user': self.user.username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'likes': self.like_set.filter(is_like=True).count(),
            'dislikes': self.like_set.filter(is_like=False).count()
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_like = models.BooleanField()  # True for like, False for dislike
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [
            ('user', 'destination'),
            ('user', 'comment')
        ]

    def __str__(self):
        target = self.destination or self.comment
        action = "likes" if self.is_like else "dislikes"
        return f"{self.user.username} {action} {target}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    interests = models.TextField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    preferred_language = models.CharField(max_length=2, choices=[
        ('en', 'English'),
        ('ru', 'Russian'),
    ], default='en')
    
    def __str__(self):
        return f"Profile of {self.user.username}" 