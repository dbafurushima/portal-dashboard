from .models import Message, Comment, Host, Locator, Application, Inventory
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['subject', 'timestamp', 'msg']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['message', 'comment', 'commented_by']


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['os_name', 'arch', 'platform', 'processor', 'hostname', 'ram', 'physical_cores', 'current_frequency']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['name', 'host']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['host', 'equipment']
