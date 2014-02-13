# coding: utf-8


ADMINS = (
    ('Artur Czepiel', 'czepiel.artur@gmail.com'),
    ('Artur Smet', 'a.smet@arturstudio.com'),
    ('Pawel Kilian', 'pawelkilian@gmail.com'),
)

MANAGERS = ADMINS

###############################################################################
###############################################################################
ROOT_URLCONF = 'wklejorg.urls'
TIME_ZONE = 'Europe/Warsaw'
LANGUAGES = [
    ('en', 'English'),
    ('pl', 'Polish'),
]
LANGUAGE_CODE = 'pl'

SITE_ID = 1
USE_I18N = True


###############################################################################
###############################################################################
import os
import sys


def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

sys.path.append(rel('../apps'))
sys.path.append(rel('../forks'))

MEDIA_ROOT = rel('../_media')
FILES_ROOT = rel('../_files')

MEDIA_URL = ''
STATIC_ROOT = rel('../_static')
STATIC_URL = '/static/'
LOCALE_PATHS = [rel('../locale')]

USE_SSL = False
USE_CAPTCHA = True

###############################################################################
###############################################################################
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

TEMPLATE_DIRS = (
    rel('../templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)


###############################################################################
###############################################################################
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'userban.middleware.BlockedIpMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'raven.contrib.django.middleware.Sentry404CatchMiddleware',
)


###############################################################################
###############################################################################
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',

    # 3rd party
    'django_extensions',
    'helpers',
    'userban',
    'registration',
    'south',
    'pagination',
    'raven.contrib.django',

    # Project specific
    'wklej',
    'userstuff',
]


###############################################################################
###############################################################################
# 3-day activation window
ACCOUNT_ACTIVATION_DAYS = 3
AUTH_PROFILE_MODULE = "userstuff.userprofile"


###############################################################################
###############################################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
