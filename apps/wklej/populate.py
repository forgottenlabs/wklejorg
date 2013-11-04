#coding: utf-8

import random
import string
from django.contrib.auth.models import User
LENGTH = 1000000


def wklejka():
    body = ''
    username = 'artur'
    user = User.objects.get(username=username)

    # create LENGTH lines, with 100 characters each
    for i in range(LENGTH):
        if i % 100 == 0:
            body += "\n"
        body += random.choice(string.ascii_uppercase + string.digits)

    return {
        "body": body,
        "user": user,
        "syntax": "text",
    }
