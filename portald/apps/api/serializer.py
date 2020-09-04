from .models import Message, Comment, Host, Locator, Application, Inventory
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'subject', 'timestamp', 'msg']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'message', 'comment', 'commented_by']


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ['id', 'os_name', 'arch', 'platform', 'processor', 'hostname', 'ram', 'cores', 'frequency']


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'name', 'host']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['id', 'host', 'equipment']
