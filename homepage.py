#-*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.conf import settings
from django.template.response import TemplateResponse
from pygments.lexers import guess_lexer
from apps.wklej.forms import WklejkaForm, WklejkaCaptchaForm
import hashlib
import random


def homepage(request):
    """
    This view is responsible for displaying form on the homepage.
    This is actualy all what it's doing. it displays, validate, and submits
    new paste into database.
    """

    if not request.method == 'POST':
        # if it's not a POST request, i just display pure homepage.dhtml
        # with empty form. When user has cookie with previously used highlight
        # he recieves form with initial syntax

        if 'highlight' in request.COOKIES:
            syntax = request.COOKIES['highlight']
            form = WklejkaForm(initial={'syntax': syntax})
        else:
            form = WklejkaForm()

        return TemplateResponse(request, 'homepage.dhtml', {'form': form})

    ### now i can focus on processing a POST request for new paste.
    try:
        if request.POST.get('has_captcha', '') and settings.USE_CAPTCHA:
            form = WklejkaCaptchaForm(request.POST)
        else:
            form = WklejkaForm(request.POST)

        if form.is_valid():
            formatka = form.save(commit=False)

            ## New in 04.
            ## Saves user ip (for spam reasons mostly)
            ## and where paste came from (statistics)
            formatka.ip = request.META['REMOTE_ADDR']
            formatka.wherefrom = "wklej.homepage"

            ### now the fun part - generating hash and other stuff
            if formatka.is_private:
                t = hashlib.sha1()
                salt = t.update(str(random.random()))
                salt = t.hexdigest()
                hash = t.update(salt)
                hash = t.hexdigest()[:11]  # 11 becuase older algo has 10

                formatka.hash = hash

            if request.user.is_authenticated():
                formatka.user = request.user

            temp = guess_lexer(formatka.body)
            formatka.guessed_syntax = temp.aliases[0]
            formatka.save()

            response = HttpResponseRedirect(formatka.get_absolute_url())
            response.set_cookie('highlight', formatka.hl)

            return response

        else:
            form = WklejkaCaptchaForm(request.POST,
                                      initial={'has_captcha': '1'})

            return TemplateResponse(request, "homepage.dhtml", {
                'form': form,
                'has_captcha': True,
                'errormsg': "Wyglądasz jak spamer. Dla pewności wpisz captchę",
            })
    except:
        return HttpResponseRedirect("/")
