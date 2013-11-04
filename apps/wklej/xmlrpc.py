#-*- coding: utf-8 -*-

# Patchless XMLRPC Service for Django
# Kind of hacky, and stolen from Crast on irc.freenode.net:#django
# Self documents as well, so if you call it from outside of an XML-RPC Client
# it tells you about itself and its methods
#
# Brendan W. McAdams <brendan.mcadams@thewintergrp.com>

# SimpleXMLRPCDispatcher lets us register xml-rpc calls w/o
# running a full XMLRPC Server.  It's up to us to dispatch data

import sha
import random
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse


# Create a Dispatcher; this handles the calls and translates info to function
# maps
#dispatcher = SimpleXMLRPCDispatcher() # Python 2.4
dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)  # Py 2.5

# model
from wklej.models import Wklejka
from userstuff.models import ProfilUzytkownika


def rpc_handler(request):
    """
    the actual handler:
    if you setup your urls.py properly, all calls to the xml-rpc service
    should be routed through here.
    If post data is defined, it assumes it's XML-RPC and tries to process as
    such Empty post assumes you're viewing from a browser and tells you about
    the service.
    """

    response = HttpResponse()
    if len(request.POST):
        response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
    else:
        response.write("<b>This is an XML-RPC Service.</b><br>")
        #methods = dispatcher.system_listMethods()
    response['Content-length'] = str(len(response.content))
    return response


def dodaj_wpis(tresc, syntax, autor="Anonim"):
    """
    Pozwala zdalnie dodawac wpisy do wkleja.
    """

    w = Wklejka(nickname=autor, body=tresc, syntax=syntax)
    w.save()

    return w.get_absolute_url()


def dodaj_prywatny_wpis(tresc, syntax, autor="Anonim"):
    """
    Pozwala zdalnie dodawać prywatne wpisy do wkleja
    """

    w = Wklejka(nickname=autor, body=tresc, syntax=syntax, is_private=True)
    w.save()
    salt = sha.new(str(random.random())).hexdigest()[:10]
    hash = sha.new(salt).hexdigest()[:10]
    w.hash = hash
    w.save()

    return w.get_absolute_url()


def auth_dodaj_wpis(tresc, syntax, salt):
    """
    Pozwala zdalnei dodawac wpisy do konta
    """
    try:
        p = ProfilUzytkownika.objects.get(aktualny_salt=salt)
    except:
        return dodaj_wpis(tresc, syntax)
    w = Wklejka(nickname=p.username(), body=tresc, syntax=syntax,  user=p.user)
    w.save()

    return w.get_absolute_url()


def auth_dodaj_prywatny_wpis(tresc, syntax, salt):
    """
    Pozwala zdalnei dodawac wpisy do konta
    """

    try:
        p = ProfilUzytkownika.objects.get(aktualny_salt=salt)
    except:
        return dodaj_prywatny_wpis(tresc, syntax)

    w = Wklejka(nickname=p.username(), body=tresc, syntax=syntax,
                user=p.user, is_private=True)
    w.save()
    salt = sha.new(str(random.random())).hexdigest()[:10]
    hash = sha.new(salt).hexdigest()[:10]
    w.hash = hash
    w.save()

    return w.get_absolute_url()


# you have to manually register all functions that are xml-rpc-able with the
# dispatcher
# the dispatcher then maps the args down.
# The first argument is the actual method, the second is what to call it from
# the XML-RPC side...
dispatcher.register_function(dodaj_wpis, 'dodaj_wpis')
dispatcher.register_function(dodaj_prywatny_wpis, 'dodaj_prywatny_wpis')
dispatcher.register_function(auth_dodaj_wpis, 'auth_dodaj_wpis')
dispatcher.register_function(auth_dodaj_prywatny_wpis,
                             'auth_dodaj_prywatny_wpis')
