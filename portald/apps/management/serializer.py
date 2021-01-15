from .models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'company_name',
            'display_name',
            'cnpj',
            'city',
            'state',
            'cep',
            'district',
            'address',
            'state_registration',
            'municipal_registration',
            'logo',
            'user',
            'mail',
            'description'
        ]
