from settings.base import *

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'new_wklej',
        "USER": 'postgres',
        "PASSWORD": 'postgres',
    },

}

LANGUAGE_CODE = 'en'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INSTALLED_APPS += ['discoverage']
TEST_RUNNER = 'discoverage.DiscoverageRunner'
SOUTH_TESTS_MIGRATE = False
