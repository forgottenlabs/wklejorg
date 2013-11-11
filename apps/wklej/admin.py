#coding: utf-8

from wklej.models import Wklejka
from django.contrib import admin


class WklejAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'syntax', 'is_private']
    search_fields = ['user', 'nickname', 'comment', 'body', 'ip']
    list_filter = ['is_private', 'is_deleted', 'is_spam']
    raw_id_fields = ['parent', ]


admin.site.register(Wklejka, WklejAdmin)
