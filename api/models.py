from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.db.models import Q
import os

def user_profile_picture_path(instance, filename):
    """Generate file path for profile picture"""
    ext = filename.split('.')[-1]
    filename = f'{instance.user.username}_profile_pic.{ext}'
    return os.path.join('profile_pics', filename)

def user_cover_photo_path(instance, filename):
    """Generate file path for cover photo"""
    ext = filename.split('.')[-1]
    filename = f'{instance.user.username}_cover_photo.{ext}'
    return os.path.join('cover_photos', filename)

class UserProfile(models.Model):
    """
    Extended user profile model that adds additional fields to the default Django User model.
    This model handles all user-specific data and relationships such as followers and profile details.
    
    Key features:
    - One-to-one relationship with Django's User model
    - Profile picture and cover photo upload
    - Bio and location information
    - Verification status
    - Follower/Following relationship management
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(
        upload_to=user_profile_picture_path,
        null=True,
        blank=True,
        max_length=255,
        help_text="Profile picture - Maximum size 5MB"
    )
    cover_photo = models.ImageField(
        upload_to=user_cover_photo_path,
        null=True,
        blank=True,
        max_length=255,
        help_text="Cover photo - Maximum size 5MB"
    )
    website = models.URLField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self, *args, **kwargs):
        """Override save method to handle image processing"""
        # Delete old profile picture if it's being replaced
        if self.pk:
            try:
                old_instance = UserProfile.objects.get(pk=self.pk)
                if old_instance.profile_picture and self.profile_picture != old_instance.profile_picture:
                    old_instance.profile_picture.delete(save=False)
                if old_instance.cover_photo and self.cover_photo != old_instance.cover_photo:
                    old_instance.cover_photo.delete(save=False)
            except UserProfile.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    @property
    def followers_count(self):
        """Returns the number of followers for this user"""
        return self.followers.count()

    @property
    def following_count(self):
        """Returns the number of users this user is following"""
        return UserProfile.objects.filter(followers=self.user).count()

@receiver(post_delete, sender=UserProfile)
def delete_user(sender, instance, **kwargs):
    """
    Signal receiver that deletes the associated User instance when a UserProfile is deleted.
    This ensures that deleting a profile also removes the user account and all related data.
    """
    try:
        user = instance.user
        user.delete()
    except User.DoesNotExist:
        pass

@receiver([post_save, post_delete], sender=User)
def handle_user_profile(sender, instance, created=None, **kwargs):
    """
    Signal handler for User model to manage associated UserProfile.
    - Creates UserProfile when User is created
    - Deletes associated data when User is deleted
    """
    if created:
        UserProfile.objects.create(user=instance)
    elif not created and kwargs.get('signal') == post_delete:
        # Clean up related data that might not be caught by cascade
        Post.objects.filter(author=instance).delete()
        Comment.objects.filter(author=instance).delete()
        Message.objects.filter(Q(sender=instance) | Q(recipient=instance)).delete()
        Notification.objects.filter(Q(sender=instance) | Q(recipient=instance)).delete()

@receiver(pre_delete, sender=UserProfile)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal handler for UserProfile deletion.
    Ensures proper cleanup of all related data before profile deletion.
    """
    user = instance.user
    
    # Clean up posts and related data
    posts = Post.objects.filter(author=user)
    for post in posts:
        post.likes.clear()  # Clear many-to-many relationships
        post.mentions.clear()
        post.hashtags.clear()
        post.delete()
    
    # Clean up comments
    comments = Comment.objects.filter(author=user)
    for comment in comments:
        comment.likes.clear()
        comment.delete()
    
    # Clean up messages
    Message.objects.filter(Q(sender=user) | Q(recipient=user)).delete()
    
    # Clean up notifications
    Notification.objects.filter(Q(sender=user) | Q(recipient=user)).delete()
    
    # Clean up social relationships
    instance.followers.clear()
    UserProfile.objects.exclude(user=user).filter(followers=user).update(followers=None)

class Post(models.Model):
    """
    Post model representing user posts in the social media platform.
    Handles text content, images, visibility settings, and social interactions.
    
    Key features:
    - Text content and optional image
    - Privacy settings (public, followers-only, private)
    - Like system
    - Hashtag support
    - User mentions
    - Share counting
    """
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
        """Returns the number of likes for this post"""
        return self.likes.count()

    @property
    def comments_count(self):
        """Returns the number of comments for this post"""
        return self.comments.count()

class Comment(models.Model):
    """
    Comment model for user comments on posts.
    Supports likes and maintains activity status.
    
    Key features:
    - Text content
    - Like system for comments
    - Timestamps for creation and updates
    - Active status tracking
    """
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
    """
    Hashtag model for categorizing and searching posts.
    Tracks usage count and creation time.
    
    Key features:
    - Unique hashtag names
    - Creation timestamp
    - Post count tracking
    """
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.name}"

    @property
    def posts_count(self):
        """Returns the number of posts using this hashtag"""
        return self.posts.count()

class Notification(models.Model):
    """
    Notification model for tracking user interactions.
    Handles different types of notifications and their read status.
    
    Notification types:
    - Likes on posts/comments
    - New comments
    - New followers
    - Mentions in posts
    - Post shares
    """
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
    """
    Direct messaging model for private communication between users.
    Tracks message status and maintains conversation history.
    
    Key features:
    - Private messaging between users
    - Read status tracking
    - Timestamp for message ordering
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"
