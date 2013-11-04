#-*- coding: utf-8 -*-

from django import http
from django.db.models import F

from userban.models import UserBan


class BlockedIpMiddleware(object):
    """
    This middleware checks for blocked ip's
    and then (if ip is blocked) return 403
    """

    def process_request(self, request):
        """forbid access for certain IP. or not"""
        banip = UserBan.objects.filter(ip=request.META['REMOTE_ADDR'],
                                       is_active_ban=True)
        if banip:
            banip.update(times_accessed=F('times_accessed')+1)
            return http.HttpResponseForbidden("<h1>Forbidden</h1>")
        return None
