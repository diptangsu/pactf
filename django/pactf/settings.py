"""Define (default) configuration for the project"""
import os
from os.path import join, dirname

from configurations import Configuration, values
from django.contrib import messages

from pactf.constants import BASE_DIR
import ctflex.constants


# TODO(Yatharth): Prefix attributes and set django-configurations prefix appropriately

class Django:
    INSTALLED_APPS = [
        # Django Defaults
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Django Extensions
        'django.contrib.postgres',

        # Django 3rd-party
        'django_countries',
        'django_extensions',
        'debug_toolbar',
        'email_log',
        'widget_tweaks',

        # Python 3rd-party
        'yaml',

        # Local
        # (pactf_web comes before ctflex to override the latter's templates.)
        'pactf_web',
        'ctflex',
    ]

    MIDDLEWARE_CLASSES = (
        # Django Defaults
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',

        # Django 3rd-party
        'ctflex.middleware.RatelimitMiddleware',
    )

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

    ROOT_URLCONF = 'pactf.urls'

    WSGI_APPLICATION = 'pactf.wsgi.application'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    # Default
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',

                    # CTFlex
                    'ctflex.views.default_context'
                ],
            },
        },
    ]

    ROOT_URLCONF = 'pactf.urls'

    WSGI_APPLICATION = 'pactf.wsgi.application'

    # URL to serve static files at
    STATIC_URL = '/static/'

    # Make connections persistent
    CONN_MAX_AGE = 60 * 60

    # Auth URLs
    LOGIN_URL = 'ctflex:login'
    LOGOUT_URL = 'ctflex:logout'
    LOGIN_REDIRECT_URL = 'ctflex:index'

    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/New_York'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Database
    # (Postgres is required for CTFlex's CtfProblem's JSONField.)
    DATABASES = values.DatabaseURLValue(environ_required=True)

    # Where to finally collect static files to
    # (Point your server (nginx, Apache etc.) to serve from this folder directly.)
    STATIC_ROOT = join(BASE_DIR, 'static')

    # Where all to collect static files from
    STATICFILES_DIRS = values.ListValue([])

    # Email
    EMAIL_HOST = values.Value('smtp.gmail.com')
    EMAIL_PORT = values.IntegerValue(587)
    DEFAULT_FROM_EMAIL = values.Value('ctflex2@gmail.com')
    SERVER_EMAIL = values.Value('ctflex2@gmail.com')
    EMAIL_HOST_USER = values.Value('ctflex2@gmail.com')
    EMAIL_HOST_PASSWORD = values.SecretValue()
    EMAIL_USE_TLS = values.BooleanValue(True)
    SUPPORT_EMAIL = 'ctflex2+support@gmail.com'  # not standard, but used by CTFlex

    # TODO(Yatharth): Uncomment when actually able to test
    RATELIMIT_VIEW = values.Value('ctflex.views.rate_limited')

    # For Boostrap Alerts
    MESSAGE_TAGS = {
        messages.ERROR: 'danger'
    }


class Security:
    SECRET_KEY = values.SecretValue()

    # Use PBKDF2PasswordHasher that uses 4 times the default number of iterations
    PASSWORD_HASHERS = ['ctflex.hashers.PBKDF2PasswordHasher4',
                        'django.contrib.auth.hashers.PBKDF2PasswordHasher']

    # Number of days that a password reset link is valid for
    PASSWORD_RESET_TIMEOUT_DAYS = 1

    # Request modern browsers to block suspected XSS attacks. Not to be relied upon.
    SECURE_BROWSER_XSS_FILTER = True

    # Prevent browsers from guessing content types (reducing security risk).
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Validation for passwords
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 7,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


class Gunicorn:
    # As whom Gunicorn should run the server
    USER = values.Value()
    GROUP = values.Value()

    # Path to Gunicorn
    GUNICORN = values.PathValue('~/.virtualenvs/pactf/bin/gunicorn')

    # Whether to use a socket or serve directly to an address
    USE_SOCKFILE = values.BooleanValue(False)

    # Socket to communicate with
    SOCKFILE = values.PathValue(join(BASE_DIR, 'run', 'gunicorn.sock'), check_exists=False)

    # Url to directly serve to
    IP = values.IPValue('127.0.0.1')
    PORT = values.IntegerValue(8001)

    # Number of worker processes Gunicorn should spawn
    NUM_WORKERS = values.IntegerValue(3)


ctflex_prefix = ctflex.constants.APP_NAME.capitalize()


class CTFlex(Django, Configuration):
    """Configure CTFlex"""

    # Directory containing problem folders
    PROBLEMS_DIR = values.Value(join(BASE_DIR, 'ctfproblems'), environ_prefix=ctflex_prefix)

    # Extras for the markdown2 Python module for formatting problem description and hints
    MARKDOWN_EXTRAS = values.TupleValue(('fenced-code-blocks', 'smarty-pants', 'spoiler'))

    ''' Static Files '''

    # Intermediate folder for storing problem static files
    # (`manage.py loadprobs` will collect files to here, and `manage.py collectstatic` will collect from here to static.)
    # (If this folder is to be inside `PROBLEMS_DIR`, prepend an underscore so it is ignored by the problem importer.)
    PROBLEMS_STATIC_DIR = join(PROBLEMS_DIR.value, '_static')

    # Subdirectory (of the directory to which static files are collected) for problems' static files
    PROBLEMS_STATIC_URL = 'ctfproblems'

    @classmethod
    def add_staticfiles_dir(cls):
        cls.STATICFILES_DIRS.append(
            (cls.PROBLEMS_STATIC_URL, cls.PROBLEMS_STATIC_DIR)
        )

    ''' General '''

    @classmethod
    def setup(cls):
        super().setup()
        cls.add_staticfiles_dir()


# TODO(Yatharth): Figure out why putting CTFlex before Security screws up SECRET_KEY
class Base(Security, CTFlex, Gunicorn, Django, Configuration):
    pass


class Dev(Base):
    # Security
    DEBUG = True
    ALLOWED_HOSTS = values.ListValue(['*'])

    # Logging
    EMAIL_BACKEND = 'email_log.backends.EmailBackend'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            # 'file': {
            #     'level': 'DEBUG',
            #     'class': 'logging.FileHandler',
            #     'f®ilename': join(BASE_DIR, 'logs', 'django.log'),
            # },
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': True,
            },
            ctflex.constants.QUERY_LOGGER: {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }


class Prod(Base):
    # Security
    DEBUG = False
    ALLOWED_HOSTS = values.ListValue(['.pactf.com', '.pactf.cf'])

    https = True  # For settings that should only be true when using HTTPS
    SESSION_COOKIE_SECURE = https
    CSRF_COOKIE_SECURE = https

    # (Only enable this if nginx is properly configured with HTTPS.)
    # SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
