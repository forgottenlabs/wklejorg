from apps.wklej.models import Wklejka
from django.contrib.auth.models import User

from django.test import TestCase


class WklejkaTestCase(TestCase):

    def test_author(self):
        user = User(username="joedoe")
        self.wklejka = Wklejka(
            user=user,
            nickname="Anonymous",
            body="Foobar",
        )
        self.assertEqual(self.wklejka.author, user)

        self.wklejka = Wklejka(
            nickname="Anonymous",
            body="Foobar",
        )
        self.assertEqual(self.wklejka.author, "Anonymous")

    def test_get_id_url(self):
        w = Wklejka()
        w.save()
        self.assertEqual(w.get_id_url(), "/id/{}/".format(w.id))

    def test_get_hash_url(self):
        w = Wklejka(hash="foobar")
        w.save()
        self.assertEqual(w.get_hash_url(), "/hash/foobar/")

    def test_get_del_url(self):
        w = Wklejka(hash="foobar", is_private=True)
        w.save()
        self.assertEqual(w.get_del_url(), "/hash/{}/delete/".format(w.hash))

        w.is_private = False
        self.assertEqual(w.get_del_url(), "/id/{}/delete/".format(w.id))

    def test_is_parent(self):
        parent = Wklejka()
        parent.save()
        self.assertFalse(parent.is_parent())

        child = Wklejka(parent=parent)
        child.save()
        self.assertTrue(parent.is_parent())

    def test_children_count(self):
        parent = Wklejka()
        parent.save()
        self.assertEquals(parent.children_count(), 0)

        child = Wklejka(parent=parent)
        child.save()
        self.assertEquals(parent.children_count(), 1)

    def test_is_child(self):
        parent = Wklejka()
        parent.save()

        child = Wklejka()
        child.save()
        self.assertFalse(child.is_child())

        child.parent = parent
        self.assertTrue(child.is_child())

    def test_get_10_lines(self):
        w = Wklejka(body="\n".join("abcdefghijklmn"))
        self.assertEqual(w.get_10_lines().splitlines()[-1], "j")

    def test_hl(self):
        w = Wklejka(syntax="python")
        self.assertEqual(w.hl, "python")

        w = Wklejka(syntax="", guessed_syntax="perl")
        self.assertEqual(w.hl, "perl")
