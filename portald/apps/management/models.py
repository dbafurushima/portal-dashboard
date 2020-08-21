from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime


class Client(models.Model):
    company_name = models.CharField(verbose_name="Razão social", max_length=100, unique=True)
    display_name = models.CharField(verbose_name="Apelido", max_length=50, blank=True)
    cnpj = models.CharField(verbose_name="CNPJ", max_length=20, blank=True)
    city = models.CharField(verbose_name="Cidade", max_length=40, blank=True)
    state = models.CharField(verbose_name="Estado", max_length=40, blank=True)
    cep = models.CharField(verbose_name="CEP", max_length=15, blank=True)
    state_registration = models.CharField(verbose_name="inscrição estadual", max_length=30, blank=True)
    municipal_registration = models.CharField(verbose_name="inscrição municipal", max_length=30, blank=True)
    logo = models.ImageField(verbose_name="logo", upload_to='logos/%d/%m/%Y/', default='default-logo.png',
                             blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        verbose_name = _('clients')
        verbose_name_plural = _('clients')

    def __str__(self):
        return "<Client: {}>".format(self.display_name)

    def __repr__(self):
        return self.__str__()


class Notification(models.Model):
    pass
