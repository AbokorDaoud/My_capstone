from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment, Hashtag, Notification, Message

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'bio', 'location', 'website', 'followers_count', 
                 'following_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with profile handling"""
    password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile', 'date_joined']
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        """Create and return a new user with encrypted password."""
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    def update(self, instance, validated_data):
        """Update and return an existing user."""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Handles username/password validation for authentication.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    Handles post creation and social interaction data.
    
    Features:
    - Content and media handling
    - Author information
    - Like and comment system
    - Hashtag processing
    - User mentions
    - Share tracking
    """
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    hashtags = HashtagSerializer(many=True, read_only=True)
    mentioned_users = UserSerializer(source='mentions', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'image', 'author_username', 'created_at', 
                 'updated_at', 'likes_count', 'comments_count', 'comments', 
                 'is_liked', 'is_active', 'visibility', 'hashtags', 
                 'mentioned_users', 'shares_count')
        read_only_fields = ('author', 'created_at', 'updated_at', 'is_active', 'shares_count')

    def get_is_liked(self, obj):
        """Check if the requesting user has liked this post"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Handles comment creation and interaction data.
    
    Features:
    - Author information
    - Like system
    - Timestamps
    - Activity status
    """
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author_username', 'created_at', 'updated_at', 
                 'is_active', 'likes_count', 'is_liked')
        read_only_fields = ('author', 'created_at', 'updated_at', 'is_active')

    def get_likes_count(self, obj):
        """Get the total number of likes for this comment"""
        return obj.likes.count()

    def get_is_liked(self, obj):
        """Check if the requesting user has liked this comment"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class HashtagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Hashtag model.
    Handles hashtag data and usage statistics.
    
    Features:
    - Hashtag name
    - Creation time
    - Usage count
    """
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Hashtag
        fields = ('id', 'name', 'created_at', 'posts_count')
        read_only_fields = ('created_at',)

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Notification model.
    Handles notification creation and delivery.
    
    Features:
    - Multiple notification types
    - Sender/recipient information
    - Related content (posts/comments)
    - Read status tracking
    """
    sender = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'sender', 'notification_type', 'post', 
                 'comment', 'created_at', 'is_read')
        read_only_fields = ('created_at',)

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    Handles direct messaging between users.
    
    Features:
    - Sender/recipient information
    - Message content
    - Read status
    - Timestamp tracking
    """
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'content', 'created_at', 'is_read')
        read_only_fields = ('created_at',)
