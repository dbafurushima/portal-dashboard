from .models import Message, Comment
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['subject', 'timestamp', 'msg']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['origin_message', 'comment_text', 'commented_by']
