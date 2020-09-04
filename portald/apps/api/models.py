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
        return f'<Message: {self.subject}:{self.msg[:25]}>'

    def __repr__(self):
        return self.__str__()


class Comment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(verbose_name="comment text", max_length=254, null=True)
    commented_by = models.ForeignKey(User, verbose_name="commented by", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)

    def __str__(self):
        return f'<Comment: {self.message.id}:{self.comment[:30]}>'


class Host(models.Model):
    os_name = models.CharField(max_length=40, verbose_name='os.name')
    arch = models.CharField(max_length=30, verbose_name='arch')
    platform = models.CharField(max_length=30, verbose_name='platform')
    processor = models.CharField(max_length=80)
    hostname = models.CharField(max_length=125, unique=True, blank=True, null=False)
    ram = models.FloatField(verbose_name='RAM')
    cores = models.IntegerField(verbose_name='physical cores')
    frequency = models.FloatField(verbose_name='current frequency')

    def __str__(self):
        return f'<Host: {self.hostname}>'


class Locator(models.Model):
    locator = models.CharField(max_length=20)
    size = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, blank=True, null=True)


class Application(models.Model):
    name = models.CharField(max_length=20)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, blank=True, null=True)


class Inventory(models.Model):
    EQUIPMENT = [
        ('virtual', 'Virtual Machine'),
        ('real', 'Physical Machine'),
        ('docker', 'Container Docker')
    ]

    host = models.ForeignKey(Host, on_delete=models.SET_NULL, blank=True, null=True)
    equipment = models.CharField(choices=EQUIPMENT, max_length=30, verbose_name='equipamento')
