# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

from pygments.lexers import get_all_lexers
all_lexers = get_all_lexers()

BANNED_LEXERS = [
    'antlr-objc',
    'raw',
    'c-objdump',
    'opa',
]


LISTA_LEXEROW = [
    ('python', "Python"),
    ('perl', "Perl"),
    ('ruby', "Ruby"),
    ('c', 'C'),
    ('bash', "Bash"),
    ('java', "Java"),
    ('html+django', "Html+Django"),
    ('xml', "XML"),
    ('mysql', "MySQL"),
    ('cpp', "C++"),
    ('js', 'JavaScript'),
] + sorted([
    (x[1][0], x[0]) for x in all_lexers if x[1][0] not in BANNED_LEXERS
])


class Wklejka(models.Model):
    """
    This model represents a single paste, both for anonymous and authenticated
    pasters.
    """

    nickname = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    body = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=45, blank=True)

    # syntax
    syntax = models.CharField(max_length=30, choices=LISTA_LEXEROW,
                              blank=True, null=True)
    guessed_syntax = models.CharField(max_length=30, blank=True, null=True)

    # inheritance:
    parent = models.ForeignKey('self', blank=True, null=True)

    # flags:
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)

    # new:
    comment = models.TextField(blank=True, null=True)
    wherefrom = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Wklejka"
        verbose_name_plural = "Wklejki"
        ordering = ['-pub_date']

    def __unicode__(self):
        return "%s at %s" % (self.autor, str(self.pub_date))

    @property
    def autor(self):
        if self.user:
            return self.user
        else:
            return self.nickname

    @models.permalink
    def get_absolute_url(self):
        if self.is_private:
            return self.get_hash_url()
        return self.get_id_url()

    def get_id_url(self):
        return ('single', None, {'id': self.id})

    def get_hash_url(self):
        return ('single', None, {'hash': self.hash})

    def get_del_url(self):
        return ('wklejka_del', None, {'wklejka_id': self.id})

    def is_parent(self):
        if self.wklejka_set.all():
            return True
        return False

    def children(self):
        return self.wklejka_set.all()

    def children_count(self):
        return self.children().count()

    def is_child(self):
        if self.parent:
            return True
        return False

    def get_10_lines(self):
        return "\n".join(self.body.splitlines()[:9])

    @property
    def hl(self):
        return (self.syntax or self.guessed_syntax)
