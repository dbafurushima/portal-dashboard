from django.db import models
import time


class Message(models.Model):
    ip = models.CharField(max_length=16, verbose_name="ip address", null=True, blank=True)
    timestamp = models.CharField(default=time.time, blank=True, max_length=30)
    msg = models.TextField(verbose_name="message")
