"""
API URL Configuration

This module defines the URL patterns specific to the API application.
It provides a RESTful interface for all social media functionality.

Available Endpoints:
1. Authentication:
   - POST /auth/register/ - Create new user account
   - POST /auth/login/ - Authenticate user and get tokens
   - POST /auth/token/ - Get JWT token
   - POST /auth/token/refresh/ - Refresh JWT token

2. User Management:
   - GET /users/ - List all users
   - POST /users/ - Create new user
   - GET /users/{id}/ - Get user details
   - PUT /users/{id}/ - Update user
   - DELETE /users/{id}/ - Delete user
   - POST /users/{id}/follow/ - Follow/unfollow user

3. Posts:
   - GET /posts/ - List all posts
   - POST /posts/ - Create new post
   - GET /posts/{id}/ - Get post details
   - PUT /posts/{id}/ - Update post
   - DELETE /posts/{id}/ - Delete post

4. Profiles:
   - GET /profiles/ - List all profiles
   - GET /profiles/{id}/ - Get profile details
   - PUT /profiles/{id}/ - Update profile

5. Messages:
   - GET /messages/ - List user's messages
   - POST /messages/ - Send new message
   - GET /messages/{id}/ - View message
   - DELETE /messages/{id}/ - Delete message

6. Notifications:
   - GET /notifications/ - List user's notifications
   - GET /notifications/{id}/ - View notification
   - DELETE /notifications/{id}/ - Delete notification

7. Feed:
   - GET /feed/ - Get personalized post feed
8. Health Check:
   - GET /healthz/ - Check API health

"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, PostViewSet, FeedView, UserProfileViewSet,
    UserRegistrationView, UserLoginView, api_root, health_check,
    FollowView, MessageViewSet, NotificationViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')  
router.register('posts', PostViewSet, basename='post')
router.register('profiles', UserProfileViewSet, basename='profile')
router.register('messages', MessageViewSet, basename='message')
router.register('notifications', NotificationViewSet, basename='notification')

app_name = 'api'

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('healthz/', health_check, name='health-check'),
    path('users/<int:pk>/follow/', FollowView.as_view(), name='follow-user'),
]
