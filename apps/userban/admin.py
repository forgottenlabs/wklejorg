#-*- coding: utf-8 -*-

from django.contrib import admin
from userban.models import UserBan


class UserBanAdmin(admin.ModelAdmin):
    list_display = ['ip', 'reason', 'is_active_ban', 'times_accessed']


admin.site.register(UserBan, UserBanAdmin)
