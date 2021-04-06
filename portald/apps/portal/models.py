import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Topic(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=25, unique=True)
    color = models.CharField(verbose_name="Cor", max_length=10, unique=True, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _('Tópico')
        verbose_name_plural = _('Tópicos')

    def __str__(self):
        return "<topic '%s'>" % self.name


class AppNote(models.Model):
    title = models.CharField(verbose_name="Titulo", max_length=50, unique=True)
    text = models.CharField(verbose_name="Texto", max_length=250)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    favorite = models.BooleanField(default=True, verbose_name="Favorito", null=True, blank=True)
    display = models.BooleanField(default=True, verbose_name="Visível", null=True, blank=True)

    class Meta:
        verbose_name = _('Anotação')
        verbose_name_plural = _('Anotações')

    def __str__(self):
        return "<note '%s'>" % self.title
