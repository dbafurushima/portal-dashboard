import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Client(models.Model):
    company_name = models.CharField(verbose_name="Razão social", max_length=100, unique=True)
    display_name = models.CharField(verbose_name="Apelido", max_length=50, blank=True)
    cnpj = models.CharField(verbose_name="CNPJ", max_length=20, blank=True)
    city = models.CharField(verbose_name="Cidade", max_length=40, blank=True)
    state = models.CharField(verbose_name="Estado", max_length=40, blank=True)
    cep = models.CharField(verbose_name="CEP", max_length=15, blank=True)
    district = models.CharField(verbose_name="Bairro", max_length=30, blank=True)
    address = models.CharField(verbose_name="Endereço", max_length=60, blank=True)
    state_registration = models.CharField(verbose_name="inscrição estadual", max_length=30, blank=True)
    municipal_registration = models.CharField(verbose_name="inscrição municipal", max_length=30, blank=True)
    logo = models.ImageField(verbose_name="logo", upload_to='logos/%d/%m/%Y/', default='default-logo.png',
                             blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    mail = models.CharField(verbose_name="E-Mail", max_length=120, blank=True, null=True)

    class Meta:
        verbose_name = _('clients')
        verbose_name_plural = _('clients')

    @property
    def cnpj_text(self):
        return self.cnpj.replace('.', '').replace('/', '').replace('-', '')

    def __str__(self):
        return "<Client: {}>".format(self.display_name)

    def __repr__(self):
        return self.__str__()


class Notification(models.Model):
    ICONS = [
        ('warning', 'alert-triangle'),
        ('complete', 'check-circle'),
        ('block-user', 'user-minus')
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    icon = models.CharField(max_length=20, choices=ICONS, blank=True, null=True)
    message = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class PasswordSafe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    password = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return f"<PS {self.user.username}:{self.password[:15]}>"


class EnterpriseUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    enterprise = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'<{self.enterprise.display_name}:{self.user.username}>'
