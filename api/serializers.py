from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'bio', 'profile_picture', 'followers', 'following', 'followers_count', 'following_count']

    def get_followers(self, obj):
        return [{'id': profile.user.id, 'username': profile.user.username} 
                for profile in obj.followers.all()]

    def get_following(self, obj):
        return [{'id': profile.user.id, 'username': profile.user.username} 
                for profile in obj.following.all()]

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'content', 'image', 'created_at', 'updated_at', 'author_username')
        read_only_fields = ('author_username', 'created_at', 'updated_at')
