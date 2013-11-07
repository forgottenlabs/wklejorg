wklejorg
========

Source code of wklej.org nopaste. Nopaste built with Django.

    $ virtualenv wklej.org
    $ cd wklej.org
    $ source bin/activate
    $ git clone https://github.com/czartur/wklejorg
    $ cd wklejorg
    $ pip install -r requirements.txt
    $ cp settings/base.py settings/local.py
    $ cat settings/local.py.example >> settings/local.py
    $ vim settings/env.py
    $ export DJANGO_SETTINGS_MODULE=settings.local
    $ ./manage.py syncdb
    $ ./manage.py migrate
    $ ./manage.py runserver

