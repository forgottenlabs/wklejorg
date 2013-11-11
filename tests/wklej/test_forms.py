from __future__ import unicode_literals

from django.test import TestCase

from wklej.forms import WklejkaForm, WklejkaCaptchaForm


class WklejkaFormTest(TestCase):

    def setUp(self):
        self.formclass = WklejkaForm

    def test_clean_nickname(self):
        form = self.formclass(data={"nickname": "", "body": "Foo"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean_nickname(), "Anonim")

        form = self.formclass(data={"nickname": "abc"*20, "body": "Foo"})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.clean_nickname()), 29)

    def test_clean_body(self):
        form = self.formclass(data={"body": "http://wklej.org"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['body'], ["This paste looks like spam."])


#class WklejkaCaptchaFormTest(TestCase):

    #def setUp(self):
        #self.formclass = WklejkaCaptchaForm

    #def test_clean_nickname(self):
        #form = self.formclass(data={"nickname": "", "body": "Foo",
                                    #"has_captcha": 0})
        #self.assertTrue(form.is_valid())
        #self.assertEqual(form.clean_nickname(), "Anonim")

        #form = self.formclass(data={"nickname": "abc"*20, "body": "Foo",
                                    #"has_captcha": 0})
        #self.assertTrue(form.is_valid())
        #self.assertEqual(len(form.clean_nickname()), 29)

    #def test_clean_body(self):
        #form = self.formclass(data={"body": "http://wklej.org",
                                    #"recaptcha_response_field": "PASSED"})
        #print form.errors
        #self.assertTrue(form.is_valid())
