from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, PostViewSet, FeedView, UserProfileViewSet,
    UserRegistrationView, UserLoginView, api_root, health_check
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')  
router.register('posts', PostViewSet, basename='post')
router.register('profiles', UserProfileViewSet, basename='profile')

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
]
