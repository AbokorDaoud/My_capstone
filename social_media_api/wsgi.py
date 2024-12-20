"""
WSGI config for social_media_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Print debugging information
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)
print("Project directory contents:", os.listdir(BASE_DIR))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_api.settings')

try:
    application = get_wsgi_application()
    print("WSGI application loaded successfully")
except Exception as e:
    print(f"Error loading application: {e}")
    print("Python path at error:", sys.path)
    print("Current directory contents:", os.listdir(os.getcwd()))
    raise