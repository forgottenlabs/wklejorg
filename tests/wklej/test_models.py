from wklej.models import Wklejka

from django.test import TestCase


class WklejkaTestCase(TestCase):
    def setUp(self):
        Wklejka()

    def test_foo(self):
        assert 1 == 1
