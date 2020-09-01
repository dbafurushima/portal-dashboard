from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .serializer import MessageSerializer, CommentSerializer, ApplicationSerializer, HostSerializer, InventorySerializer
from .models import Message, Comment, Application, Host, Inventory
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


class CommentViewSet(viewsets.ModelViewSet):
    """show all comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
