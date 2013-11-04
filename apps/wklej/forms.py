#-*- coding: utf-8 -*-

from django import forms
from wklej.models import Wklejka
from wklejorg.lib.antispam import check_for_link_spam
from recaptcha_app.fields import ReCaptchaField
from wklej.models import LISTA_LEXEROW


class WklejkaForm(forms.ModelForm):
    nickname = forms.CharField(required=False)

    def clean_nickname(self):
        if len(self.cleaned_data['nickname']) == 0:
            self.cleaned_data['nickname'] = 'Anonim'
        elif len(self.cleaned_data['nickname']) > 30:
            self.cleaned_data['nickname'] = self.cleaned_data['nickname'][:29]

        return self.cleaned_data['nickname']

    class Meta:
        model = Wklejka

    def clean_body(self):
        if check_for_link_spam(self.cleaned_data['body']):
            raise forms.ValidationError("This paste looks like spam.")
        return self.cleaned_data['body']


# TODO: FIXME: Do this with inheritance
class WklejkaCaptchaForm(forms.ModelForm):
    recaptcha = ReCaptchaField()
    has_captcha = forms.CharField(widget=forms.HiddenInput, required=False)
    nickname = forms.CharField(required=False)

    def clean_nickname(self):
        if len(self.cleaned_data['nickname']) == 0:
            self.cleaned_data['nickname'] = 'Anonim'
        elif len(self.cleaned_data['nickname']) > 30:
            self.cleaned_data['nickname'] = self.cleaned_data['autor'][:29]

        return self.cleaned_data['nickname']

    class Meta:
        model = Wklejka


### To change syntax hilight on "single" page.
class RotateSyntaxForm(forms.Form):
    hl = forms.CharField(max_length=100, label="syntax ",
                         widget=forms.Select(choices=LISTA_LEXEROW))
