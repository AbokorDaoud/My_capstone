from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment, Hashtag, Notification, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user, is_verified=False)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'bio', 'profile_picture', 'is_verified', 'created_at', 
                 'updated_at', 'followers_count', 'following_count', 'is_following',
                 'website', 'location', 'cover_photo')
        read_only_fields = ('created_at', 'updated_at', 'is_verified')

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author_username', 'created_at', 'updated_at', 
                 'is_active', 'likes_count', 'is_liked')
        read_only_fields = ('author', 'created_at', 'updated_at', 'is_active')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class HashtagSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Hashtag
        fields = ('id', 'name', 'created_at', 'posts_count')
        read_only_fields = ('created_at',)

class PostSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'sender', 'notification_type', 'post', 
                 'comment', 'created_at', 'is_read')
        read_only_fields = ('created_at',)

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'content', 'created_at', 'is_read')
        read_only_fields = ('created_at',)
