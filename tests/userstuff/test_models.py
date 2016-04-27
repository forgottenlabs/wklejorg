from apps.userstuff.models import UserProfile
from apps.wklej.models import Wklejka
from django.contrib.auth.models import User

from django.test import TestCase


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User(username="foobar")
        self.user.save()
        self.wklejka = Wklejka(user=self.user, body="foobarbaz").save()
        self.userprofile = UserProfile(user=self.user)
        self.userprofile.save()

    def test_username(self):
        self.assertEquals(self.userprofile.username(), "foobar")

    def test_get_wklejki(self):
        wklejki = self.userprofile.get_wklejki().all()
        self.assertEquals(wklejki.count(), 1)
        self.assertEquals(wklejki[0].body, "foobarbaz")

    def test_generate_new_salt(self):
        userprofile_id = self.userprofile.id
        new_salt = self.userprofile.generate_new_salt()
        new_profile = UserProfile.objects.get(current_salt=new_salt)
        self.assertEqual(userprofile_id, new_profile.id)
