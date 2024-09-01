"""
Django settings file

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Current environment (LOCAL/DEV)
ENVIRONMENT = os.environ.get("ENVIRONMENT")

# Set debug mode to True only in the local environment
DEBUG = ENVIRONMENT == "LOCAL"

SECRET_KEY = os.environ.get("SECRET_KEY")

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "polls.apps.PollsConfig"  # Sample polls app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # If you change the path to the SQLite file in the LOCAL environment, update it
        # also in the "postCreateCommand" command in ".devcontainer/devcontainer.json".
        "NAME": os.path.join(BASE_DIR.parent, ".database", "db.sqlite3"),
    }
}

# Use file-based sessions
SESSION_ENGINE = "django.contrib.sessions.backends.file"

# If no SESSION_FILE_PATH set, the session files will be stored in tempfile.gettempdir(),
# which most likely is `/tmp`
# SESSION_FILE_PATH = None


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# A simple configuration to output all log messages to the console
# https://docs.djangoproject.com/en/5.0/topics/logging/#examples
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Settings for remote environments
if ENVIRONMENT != "LOCAL":
    # This is *only* for the development environment: "*" will match any host
    ALLOWED_HOSTS.append("*")

    # Path to EFS
    MOUNTED_FILE_SYSTEM_PATH = Path(os.environ.get("MOUNTED_FILE_SYSTEM_PATH"))

    # Static files directory on EFS
    STATIC_ROOT = MOUNTED_FILE_SYSTEM_PATH / "staticfiles"

    # SQLite file on EFS
    DATABASES['default']['NAME'] = MOUNTED_FILE_SYSTEM_PATH / "database" / "db.sqlite3"

    # Session files directory on EFS
    SESSION_FILE_PATH = MOUNTED_FILE_SYSTEM_PATH / "session"

    # Create the session files directory if it doesn't exist and set the permissions
    SESSION_FILE_PATH.mkdir(parents=True, exist_ok=True, mode=0o750)
