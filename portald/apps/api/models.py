from django.db import models
import time
import datetime
from django.contrib.auth.models import User
from apps.management.models import Client


class Note(models.Model):
    subject = models.CharField(max_length=100, verbose_name="subject", null=True, blank=True)
    timestamp = models.CharField(default=time.time, blank=True, max_length=30)
    msg = models.TextField(verbose_name="message")
    read = models.BooleanField(verbose_name='lido', default=False, blank=True, null=True)
    deleted = models.BooleanField(default=False, blank=True, null=True)
    read_in = models.DateTimeField(blank=True, null=True)
    read_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'<Note: [{self.subject}] {self.msg[:25]}>'

    def __repr__(self):
        return self.__str__()

    class Meta:
        verbose_name_plural = "Anotações"


class Inventory(models.Model):
    enterprise = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"<Inventory: {self.enterprise.company_name}>"

    class Meta:
        verbose_name_plural = "Inventários"


class Environment(models.Model):
    name = models.CharField(verbose_name="ambiente", max_length=50)
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'<Environment: {self.name}>'

    class Meta:
        verbose_name_plural = "Ambientes"


class Host(models.Model):
    EQUIPMENT = [
        ('virtual', 'Virtual Machine'),
        ('real', 'Physical Machine'),
        ('docker', 'Container Docker')
    ]

    environment = models.ForeignKey(Environment, on_delete=models.SET_NULL, blank=True, null=True)

    private_ip = models.CharField(max_length=16, verbose_name="ip privado", blank=True, null=True)
    public_ip = models.CharField(max_length=16, verbose_name="ip público", blank=True, null=True)
    os_name = models.CharField(max_length=40, verbose_name='os.name')
    arch = models.CharField(max_length=30, verbose_name='arch')
    platform = models.CharField(max_length=100, verbose_name='platform')
    processor = models.CharField(max_length=80)
    hostname = models.CharField(max_length=125, unique=True, blank=True, null=False)
    ram = models.FloatField(verbose_name='RAM')
    cores = models.IntegerField(verbose_name='physical cores')
    frequency = models.FloatField(verbose_name='current frequency', null=True, blank=True)
    equipment = models.CharField(choices=EQUIPMENT, max_length=30, verbose_name='equipamento', blank=True, null=True)

    def __str__(self):
        return f'<Host: {self.hostname}>'

    class Meta:
        verbose_name_plural = "Hosts"


class Locator(models.Model):
    locator = models.CharField(max_length=20)
    size = models.IntegerField(blank=True, null=True)
    speed = models.IntegerField(blank=True, null=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, blank=True, null=True)


class Application(models.Model):
    name = models.CharField(max_length=20)
    port = models.IntegerField(blank=True, null=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name}:{self.port}"

    class Meta:
        verbose_name_plural = "Aplicações"


class Comment(models.Model):
    comment = models.CharField(verbose_name="comment text", max_length=254, null=True)
    commented_by = models.ForeignKey(User, verbose_name="commented by", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True, null=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'<Comment: {self.note.msg[:20]}{self.comment[:30]}>'

    class Meta:
        verbose_name_plural = "Comentários"


class Service(models.Model):
    name = models.CharField(verbose_name="service", max_length=50)
    ip = models.CharField(max_length=16, null=True, blank=True)
    port = models.IntegerField(blank=True, null=True)
    dns = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return f'<Service: {self.name}>'

    class Meta:
        verbose_name_plural = "Serviços"


class Instance(models.Model):
    name = models.CharField(verbose_name="instance name", max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE, blank=True, null=True)
    hostname = models.CharField(max_length=125, unique=True, blank=True, null=False)
    private_ip = models.CharField(max_length=16, verbose_name="ip privado", blank=True, null=True)

    def __str__(self):
        return f'<Instance:  {self.name}>'

    class Meta:
        verbose_name_plural = "Instâncias"
