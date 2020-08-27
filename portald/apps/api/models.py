from django.db import models
import time


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="subject", null=True, blank=True)
    timestamp = models.CharField(default=time.time, blank=True, max_length=30)
    msg = models.TextField(verbose_name="message")
    read = models.BooleanField(verbose_name='lido', default=False, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    read_in = models.DateTimeField(blank=True, null=True)
