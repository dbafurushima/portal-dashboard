from django.db import models
import time
import datetime
from django.contrib.auth.models import User


class Message(models.Model):
    subject = models.CharField(max_length=100, verbose_name="subject", null=True, blank=True)
    timestamp = models.CharField(default=time.time, blank=True, max_length=30)
    msg = models.TextField(verbose_name="message")
    read = models.BooleanField(verbose_name='lido', default=False, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    read_in = models.DateTimeField(blank=True, null=True)
    read_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'<Message: {self.subject}:{self.msg[:15]}>'

    def __repr__(self):
        return self.__str__()


class Comment(models.Model):
    origin_message = models.ForeignKey(Message, on_delete=models.SET_NULL, blank=True, null=True)
    comment_text = models.TextField(verbose_name="comment")
    commented_by = models.CharField(max_length=30, verbose_name='commented by', null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)

    def __str__(self):
        return f'<Comment: {self.origin_message}:{self.comment_text[:30]}>'

    def __repr__(self):
        return self.__str__()
