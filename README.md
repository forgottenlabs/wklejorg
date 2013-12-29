wklejorg
========

Source code of wklej.org nopaste. Nopaste built with Django.

## Setup

    virtualenv wklej.org
    cd wklej.org
    source bin/activate
    git clone https://github.com/czartur/wklejorg
    cd wklejorg
    cp settings/base.py settings/local.py
    cat settings/local.py.example >> settings/local.py
    vim settings/env.py
    pip install -r requirements.txt
    export DJANGO_SETTINGS_MODULE=settings.local
    ./manage.py syncdb

# Every time you update

    pip install -r requirements.txt
    export DJANGO_SETTINGS_MODULE=settings.local
    ./manage.py compilemessages
    ./manage.py migrate

## To start the webapp

    ./manage.py runserver

