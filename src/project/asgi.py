"""
ASGI config for main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from blacknoise import BlackNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

# Wrap the Django ASGI application around BlackNoise
# https://github.com/matthiask/blacknoise
application = BlackNoise(get_asgi_application())
# Add the static path
application.add(
    os.path.join(os.environ.get("MOUNTED_FILE_SYSTEM_PATH"), "staticfiles"),
    "/static"
)
