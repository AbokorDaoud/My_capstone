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
from django.db.models import Q

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    API root endpoint that provides links to all main endpoints.
    Serves as the entry point and documentation for the API.
    """
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
    """
    View for handling user registration.
    
    Endpoints:
    POST /api/register/ - Create new user
    
    Features:
    - User creation
    - JWT token generation
    - Refresh token support
    """
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
    """
    View for handling user authentication and token generation.
    
    Endpoints:
    POST /api/login/ - Authenticate user and return JWT tokens
    
    Features:
    - Username/password authentication
    - JWT token generation
    - Refresh token support
    """
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
    """
    View for handling follow/unfollow actions between users.
    
    Endpoints:
    POST /api/follow/{id}/ - Follow/unfollow user
    
    Features:
    - Follow/unfollow functionality
    - Authentication required
    """
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
    """
    ViewSet for managing user accounts and social interactions.
    
    Endpoints:
    - GET /api/users/ - List all users
    - POST /api/users/ - Create new user
    - GET /api/users/{id}/ - Retrieve user details
    - PUT/PATCH /api/users/{id}/ - Update user
    - DELETE /api/users/{id}/ - Delete user
    - POST /api/users/{id}/follow/ - Follow/unfollow user
    - GET /api/users/{id}/feed/ - Get user's feed
    
    Features:
    - User CRUD operations
    - Follow/unfollow functionality
    - Personalized feed generation
    - Authentication required for most actions
    """
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
        """Handle follow/unfollow actions between users"""
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
        """Get personalized feed of posts from followed users"""
        user = self.get_object()
        following_profiles = UserProfile.objects.filter(followers=user)
        following_users = [profile.user for profile in following_profiles]
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts and their interactions.
    
    Endpoints:
    - GET /api/posts/ - List all posts
    - POST /api/posts/ - Create new post
    - GET /api/posts/{id}/ - Retrieve post
    - PUT/PATCH /api/posts/{id}/ - Update post
    - DELETE /api/posts/{id}/ - Delete post
    - POST /api/posts/{id}/like/ - Like/unlike post
    - POST /api/posts/{id}/comment/ - Comment on post
    - POST /api/posts/{id}/share/ - Share post
    
    Features:
    - Post CRUD operations
    - Hashtag processing
    - User mentions
    - Like/comment/share functionality
    - Notification generation
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Create post with hashtag and mention processing"""
        content = self.request.data.get('content', '')
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, content)
        
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, content)
        
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
        """Handle like/unlike actions on posts"""
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
        """Add comment to post and notify author"""
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'request': request})
        
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
                CommentSerializer(comment, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Handle post sharing and notify original author"""
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
        """Get comments for a post"""
        try:
            post = self.get_object()
            comments = Comment.objects.filter(post=post, is_active=True)
            serializer = CommentSerializer(comments, many=True, context={'request': request})
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(
                {'detail': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class FeedView(generics.ListAPIView):
    """
    View for retrieving personalized feed of posts.
    
    Endpoints:
    GET /api/feed/ - Get feed
    
    Features:
    - Personalized feed generation
    - Authentication required
    """
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Get personalized feed of posts for authenticated users or public posts for others"""
        if not self.request.user.is_authenticated:
            # Return public posts for unauthenticated users
            return Post.objects.filter(visibility='public').order_by('-created_at')
            
        try:
            # Try to get personalized feed for authenticated users
            user_profile = self.request.user.profile
            following_users = user_profile.followers.all()
            following_users_ids = [user.id for user in following_users]
            following_users_ids.append(self.request.user.id)  # Include user's own posts
            return Post.objects.filter(
                author_id__in=following_users_ids
            ).order_by('-created_at')
        except AttributeError:
            # If user has no profile, return only their own posts and public posts
            return Post.objects.filter(
                Q(author=self.request.user) | Q(visibility='public')
            ).order_by('-created_at')

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring service status
    """
    return Response({"status": "healthy"}, status=status.HTTP_200_OK)

class HealthCheckView(APIView):
    """
    View for health check endpoint.
    
    Endpoints:
    GET /api/health-check/ - Health check
    
    Features:
    - Service status monitoring
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.
    
    Endpoints:
    - GET /api/profiles/ - List all profiles
    - POST /api/profiles/ - Create new profile
    - GET /api/profiles/{id}/ - Retrieve profile
    - PUT/PATCH /api/profiles/{id}/ - Update profile
    - DELETE /api/profiles/{id}/ - Delete profile
    
    Features:
    - Profile CRUD operations
    - Authentication required for most actions
    """
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
    """
    ViewSet for handling direct messages between users.
    
    Endpoints:
    - GET /api/messages/ - List user's messages
    - POST /api/messages/ - Send new message
    - GET /api/messages/{id}/ - View message
    - DELETE /api/messages/{id}/ - Delete message
    
    Features:
    - Private messaging
    - Message threading
    - Read status tracking
    - Conversation history
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter messages to show only those involving the current user"""
        return Message.objects.filter(
            recipient=self.request.user
        ) | Message.objects.filter(
            sender=self.request.user
        )

    def perform_create(self, serializer):
        """Create new message with current user as sender"""
        serializer.save(sender=self.request.user)

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user notifications.
    
    Endpoints:
    - GET /api/notifications/ - List user's notifications
    - GET /api/notifications/{id}/ - View notification
    - POST /api/notifications/{id}/mark_read/ - Mark as read
    - DELETE /api/notifications/{id}/ - Delete notification
    
    Features:
    - Multiple notification types
    - Read status tracking
    - Automatic notification generation
    - Filtered to current user
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter notifications to show only those for the current user"""
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'detail': 'Notification marked as read'})
