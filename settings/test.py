from settings.base import *

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.sqlite3',
        "NAME": "test.db",
    },
}


LANGUAGE_CODE = 'en'
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INSTALLED_APPS += ['discoverage']
TEST_RUNNER = 'discoverage.DiscoverageRunner'
SOUTH_TESTS_MIGRATE = False
GOOGLE_ANALYTICS_ID = ''
COVERAGE_OMIT_MODULES = ['*test*', '*migrations*']
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_PUBLIC_KEY = ''

import os
os.environ['RECAPTCHA_TESTING'] = 'True'
