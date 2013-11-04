#-*- coding: utf-8 -*-
from random import choice
import string

SALT_LEVEL = string.ascii_lowercase + string.ascii_uppercase +\
    string.digits + string.punctuation


def generuj_salt():
    salt = ''.join([choice(SALT_LEVEL) for i in range(50)])
    return salt
