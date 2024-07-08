"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os

from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponseForbidden
from .events import event_handler


def password_change_forbidden(request):  # pylint: disable=unused-argument
    """Forbid password change in the demo version. This view is for the live demo only."""
    return HttpResponseForbidden("Password change is not allowed in the demo version.")


urlpatterns = [
    # Polls app URLs
    path("", include("polls.urls")),
    # This path is for the live demo only and should be removed along with the corresponding view
    path("admin/password_change/", password_change_forbidden),
    # Admin urls
    path("admin/", admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.ENVIRONMENT == "DEV":
    # In the development environment, add a URL that processes event payloads through
    # non-http triggers via the Lambda Web Adapter.
    #
    # Remove the leading slash from the provided path.
    urlpatterns.append(
        path(os.environ.get("AWS_LWA_PASS_THROUGH_PATH")[1:], event_handler),
    )
