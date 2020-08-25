from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .serializer import MessageSerializer
from .models import Message
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def status_route(request):
    return JsonResponse({'code': 200, 'msg': 'up'})


class MessageViewSet(viewsets.ModelViewSet):
    """show all messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
