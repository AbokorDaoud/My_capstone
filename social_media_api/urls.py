"""
URL configuration for social_media_api project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import JsonResponse
from rest_framework.documentation import include_docs_urls

admin.site.site_header = 'Social Media Admin'
admin.site.site_title = 'Social Media Admin Portal'
admin.site.index_title = 'Welcome to Social Media Admin Portal'

def healthz(request):
    return JsonResponse({"status": "healthy"}, status=200)

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    path('admin/', admin.site.urls),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('docs/', include_docs_urls(title='Social Media API')),
    path('healthz/', healthz, name='healthz'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
