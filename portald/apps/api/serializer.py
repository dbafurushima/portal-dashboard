from .models import Note, Comment, Host, Inventory, Application, Instance, Environment, Service
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'subject', 'timestamp', 'msg']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'note', 'comment']


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['id', 'os_name', 'arch', 'platform', 'processor', 'hostname', 'ram',
                  'cores', 'frequency', 'environment', 'equipment']


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ['id', 'service', 'host', 'hostname', 'private_ip']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'enterprise']


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = ['id', 'name', 'inventory']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'name', 'port', 'host']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'port', 'dns']
