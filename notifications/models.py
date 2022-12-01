from __future__ import unicode_literals

from django.conf import settings
from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    image = models.ImageField(upload_to='uploads/notification', null=True, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="notification_members")
    sent_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notification_sender", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notifications'

