
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from apps.wklej.models import Wklejka
from apps.userstuff.models import UserProfile


class TestViews(TestCase):

    def setUp(self):
        self.user = User(username="joe")
        self.user.set_password('doe')
        self.user.save()

    def get(self, obj):
        url = obj.get_absolute_url()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "wklej/single.dhtml")

    def get_txt(self, obj):
        url = obj.get_txt_url()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response._headers['content-type'],
                          ('Content-Type', 'text/plain; charset=utf-8'))

    def get_dl(self, obj):
        url = obj.get_download_url()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response._headers['content-type'],
            ('Content-Type', 'application/x-force-download')
        )

    def get_del(self, obj):
        self.client.login(username='joe', password='doe')
        url = obj.get_del_url()
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "delete.dhtml")

    def post_del(self, obj):
        self.client.login(username='joe', password='doe')
        url = obj.get_del_url()
        response = self.client.post(url, {"yes": "true"})
        self.assertEquals(response.status_code, 302)

        new_obj = Wklejka.objects.get(pk=obj.id)
        self.assertTrue(new_obj.is_deleted)
        self.assertEquals(new_obj.body, "[deleted]")

    def test_public_url(self):
        w = Wklejka(is_private=False, user=self.user)
        w.save()
        self.get(w)
        self.get_txt(w)
        self.get_dl(w)
        self.get_del(w)
        self.post_del(w)

    def test_private_url(self):
        w = Wklejka(is_private=True, hash="foobar", user=self.user)
        w.save()
        self.get(w)
        self.get_txt(w)
        self.get_dl(w)
        self.get_del(w)
        self.post_del(w)

    def test_banned_lexer(self):
        w = Wklejka(syntax="raw")
        w.save()
        self.get(w)

    def test_re(self):
        w = Wklejka()
        w.save()
        url = reverse("reply", kwargs={"id": w.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage.dhtml")

    def test_own(self):
        url = reverse("own")
        self.client.login(username='joe', password='doe')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "wklej/list.dhtml")

    def test_salt(self):
        userprofile = UserProfile(user=self.user)
        userprofile.save()
        salt = userprofile.current_salt

        self.client.login(username='joe', password='doe')
        url = reverse("salt")

        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "salt.dhtml")

        response = self.client.post(url, {'yes': 'true'})

        userprofile = UserProfile.objects.get(pk=userprofile.id)
        self.assertNotEquals(userprofile.current_salt, salt)
