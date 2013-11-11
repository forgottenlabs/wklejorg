from userstuff.models import UserProfile

from django.test import TestCase


class UserProfileTest(TestCase):
    def setUp(self):
        UserProfile()

    def test_bar(self):
        self.assertEquals(0, 0)

