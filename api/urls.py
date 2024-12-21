from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet, PostViewSet, FeedView, UserProfileViewSet,
    UserRegistrationView, UserLoginView, api_root
)

router = DefaultRouter(root_renderers=None)  # Disable default API root view
router.register(r'users', UserViewSet, basename='user')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'profiles', UserProfileViewSet, basename='profile')

app_name = 'api'  # Add namespace to avoid URL name conflicts

urlpatterns = [
    path('', api_root, name='api-root'),
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
