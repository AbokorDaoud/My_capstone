from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return UserProfile.objects.filter(followers=self.user).count()

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('followers', 'Followers Only'),
        ('private', 'Private'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    is_active = models.BooleanField(default=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    hashtags = models.ManyToManyField('Hashtag', related_name='posts', blank=True)
    mentions = models.ManyToManyField(User, related_name='mentioned_in', blank=True)
    shares_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.username}'s post: {self.content[:50]}"

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.name}"

    @property
    def posts_count(self):
        return self.posts.count()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('follow', 'Follow'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('mention', 'Mention'),
        ('share', 'Share'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.recipient.username} from {self.sender.username}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"

    class Meta:
        ordering = ['-created_at']
