from django.db import models


class UserBan(models.Model):
    ip = models.CharField(max_length=20, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active_ban = models.BooleanField(default=True)
    times_accessed = models.PositiveIntegerField(default=0)
    reason = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return self.ip
