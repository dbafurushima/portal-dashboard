from django.db import models
import datetime


class Message(models.Model):
    ip = models.CharField(max_length=16, verbose_name="ip address", null=True, blank=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now, blank=True)
    msg = models.TextField(verbose_name="message")
