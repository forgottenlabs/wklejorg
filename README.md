wklejorg
========

Source code of wklej.org nopaste. Nopaste built with Django.

    $ virtualenv wklej.org
    $ cd wklej.org
    $ source bin/activate
    $ git clone https://github.com/czartur/wklejorg
    $ cd wklejorg
    $ pip install -r requirements.txt
    $ cp env.py.example env.py
    $ vim env.py
    $ ./manage.py syncdb
    $ ./manage.py migrate
    $ ./manage.py runserver
