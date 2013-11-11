from django.db import models
from django.contrib.auth.models import User
from helpers.helpers import generate_salt


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    nazwa_wyswietlana = models.CharField(max_length=30)
    current_salt = models.CharField(max_length=50)

    def __unicode__(self):
        return self.user.username

    def username(self):
        return self.user.username

    def get_wklejki(self):
        return self.user.wklejka_set

    def get_liczba_wklejek(self):
        return self.get_wklejki().count()

    def generate_new_salt(self):
        new_salt = generate_salt()
        self.current_salt = new_salt
        self.save()
        return new_salt
