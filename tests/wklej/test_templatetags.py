from wklej.templatetags.helpers import google_analytics_id

from django.conf import settings

from django.test import TestCase


class GoogleAnalyticsTest(TestCase):

    def test_google_analytics_id(self):
        self.assertEqual(google_analytics_id(), settings.GOOGLE_ANALYTICS_ID)
