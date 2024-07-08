"""
A module that handles non-HTTP event triggers received via the Lambda Web Adapter

https://github.com/awslabs/aws-lambda-web-adapter#non-http-event-triggers
"""

import json
import logging
import secrets
from io import StringIO
from pathlib import Path

from django.conf import settings
from django.core import management
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def migrate_command():
    """
    Migrate the database

    Running management commands from your code
    https://docs.djangoproject.com/en/5.0/ref/django-admin/#running-management-commands-from-your-code
    """
    # Create the parent directories if they don't exist and set the permissions
    path = Path(settings.DATABASES['default']['NAME'])
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o750)
    # Run the command
    stdout = StringIO()
    management.call_command("migrate", stdout=stdout, stderr=stdout)
    output_string = stdout.getvalue()
    logger.info(output_string)


def create_superuser_command():
    """Create a superuser"""
    default_superuser = "root"
    user_model = get_user_model()
    if user_model.objects.exists():
        logger.warning("This command can only be run on a new database")
    else:
        password = secrets.token_urlsafe(16)
        user_model.objects.create_superuser(
            username=default_superuser,
            password=password
        )
        logger.info("Superuser created. Change the password once logged in.")
        logger.info("Username: %s, password: %s", default_superuser, password)


def collectstatic_command():
    """Collect static files"""
    # Create the directory if it doesn't exist and set the permissions
    Path(settings.STATIC_ROOT).mkdir(parents=True, exist_ok=True, mode=0o750)
    # Run the command
    stdout = StringIO()
    # collectstatic
    # https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#django-admin-collectstatic
    management.call_command("collectstatic", "--no-input", stdout=stdout, stderr=stdout)
    output_string = stdout.getvalue()
    logger.info(output_string)


@csrf_exempt
def event_handler(request):  # pylint: disable=unused-argument
    """Event handler"""
    try:
        payload = json.loads(request.body)
        manage_command = payload.get('manage')
        if manage_command not in {"migrate", "create_superuser", "collectstatic"}:
            raise ValueError("Unsupported command")
        command_functions = {
            "migrate": migrate_command,
            "create_superuser": create_superuser_command,
            "collectstatic": collectstatic_command,
        }
        command_functions[manage_command]()
    except json.JSONDecodeError:
        logger.error("Invalid JSON payload")
        return HttpResponse()
    except ValueError as ve:
        logger.error(ve)
        return HttpResponse()
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error while executing command: %s", e)
        return HttpResponse()
    return HttpResponse()
