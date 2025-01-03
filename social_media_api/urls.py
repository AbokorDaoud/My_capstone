"""
Social Media API URL Configuration

This module defines the URL patterns for the social media API.
It includes routes for user management, posts, profiles, messaging,
and notifications.

URL Structure:
- /api/ - API root and documentation
- /api/users/ - User management endpoints
- /api/posts/ - Post management endpoints
- /api/profiles/ - Profile management endpoints
- /api/messages/ - Direct messaging endpoints
- /api/notifications/ - Notification endpoints
- /api/auth/ - Authentication endpoints
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView, RedirectView
from django.http import JsonResponse

admin.site.site_header = 'Social Media Admin'
admin.site.site_title = 'Social Media Admin Portal'
admin.site.index_title = 'Welcome to Social Media Admin Portal'

def healthz(request):
    return JsonResponse({"status": "ok"})

def get_csrf_token(request):
    """
    View to get CSRF token. This is needed for non-browser clients
    that need to make POST requests.
    """
    return JsonResponse({'detail': 'CSRF cookie set'})

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('csrf/', ensure_csrf_cookie(get_csrf_token), name='csrf'),
    path('healthz/', healthz, name='healthz'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
