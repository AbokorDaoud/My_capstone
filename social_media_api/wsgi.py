"""
WSGI config for social_media_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/abokor/My_capstone'
if path not in sys.path:
    sys.path.append(path)

# Set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'social_media_api.settings'

# Set up django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()