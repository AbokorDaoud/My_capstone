from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from .models import Post, UserProfile, Comment, Hashtag, Notification, Message
from .serializers import (
    UserSerializer, PostSerializer, UserProfileSerializer,
    UserLoginSerializer, CommentSerializer, HashtagSerializer,
    NotificationSerializer, MessageSerializer
)
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
import re

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'users': reverse('api:user-list', request=request, format=format),
        'posts': reverse('api:post-list', request=request, format=format),
        'profiles': reverse('api:profile-list', request=request, format=format),
        'feed': reverse('api:feed', request=request, format=format),
        'register': reverse('api:register', request=request, format=format),
        'login': reverse('api:login', request=request, format=format),
        'health-check': reverse('api:health-check', request=request, format=format),
    })

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            user_to_follow = User.objects.get(pk=pk)
            
            if user_to_follow == request.user:
                return Response(
                    {"detail": "You cannot follow yourself."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            follower_profile, _ = UserProfile.objects.get_or_create(user=request.user)
            following_profile, _ = UserProfile.objects.get_or_create(user=user_to_follow)
            
            if following_profile in follower_profile.following.all():
                return Response(
                    {"detail": "You are already following this user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            follower_profile.following.add(following_profile)
            follower_profile.save()
            
            return Response(
                {"detail": f"You are now following {user_to_follow.username}"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def options(self, request, pk):
        return Response(status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        user = request.user
        
        if user == user_to_follow:
            return Response(
                {'detail': 'You cannot follow yourself'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile = UserProfile.objects.get(user=user_to_follow)
        
        if profile.followers.filter(id=user.id).exists():
            profile.followers.remove(user)
            return Response({'detail': f'You have unfollowed {user_to_follow.username}'})
        else:
            profile.followers.add(user)
            # Create notification for follow
            Notification.objects.create(
                recipient=user_to_follow,
                sender=user,
                notification_type='follow'
            )
            return Response({'detail': f'You are now following {user_to_follow.username}'})

    @action(detail=True, methods=['get'])
    def feed(self, request, pk=None):
        user = self.get_object()
        following_profiles = UserProfile.objects.filter(followers=user)
        following_users = [profile.user for profile in following_profiles]
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Extract hashtags from content
        content = self.request.data.get('content', '')
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, content)
        
        # Extract mentions from content
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, content)
        
        # Create post
        post = serializer.save(author=self.request.user)
        
        # Process hashtags
        for tag_name in hashtags:
            hashtag, _ = Hashtag.objects.get_or_create(name=tag_name.lower())
            post.hashtags.add(hashtag)
        
        # Process mentions
        for username in mentions:
            try:
                mentioned_user = User.objects.get(username=username)
                post.mentions.add(mentioned_user)
                # Create notification for mention
                Notification.objects.create(
                    recipient=mentioned_user,
                    sender=self.request.user,
                    notification_type='mention',
                    post=post
                )
            except User.DoesNotExist:
                continue

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'detail': 'Post unliked'})
        else:
            post.likes.add(user)
            # Create notification for like
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=user,
                    notification_type='like',
                    post=post
                )
            return Response({'detail': 'Post liked'})

    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            comment = serializer.save(
                post=post,
                author=request.user
            )
            # Create notification for comment
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    notification_type='comment',
                    post=post,
                    comment=comment
                )
            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        post = self.get_object()
        post.shares_count += 1
        post.save()
        
        # Create notification for share
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                notification_type='share',
                post=post
            )
        
        return Response({'detail': 'Post shared successfully'})

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        try:
            post = self.get_object()
            comments = Comment.objects.filter(post=post, is_active=True)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            # Return public posts for unauthenticated users
            return Post.objects.filter(visibility='public').order_by('-created_at')
            
        # Return personalized feed for authenticated users
        user_profile = self.request.user.userprofile
        following_users = user_profile.following.all()
        following_users_ids = [profile.user.id for profile in following_users]
        following_users_ids.append(self.request.user.id)  # Include user's own posts
        return Post.objects.filter(
            author_id__in=following_users_ids
        ).order_by('-created_at')

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring service status
    """
    return Response({"status": "healthy"}, status=status.HTTP_200_OK)

class HealthCheckView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == "me":
            return self.request.user.profile
        return super().get_object()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            recipient=self.request.user
        ) | Message.objects.filter(
            sender=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read'})
