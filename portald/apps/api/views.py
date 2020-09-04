from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .serializer import MessageSerializer, CommentSerializer, ApplicationSerializer, HostSerializer, InventorySerializer
from .models import Message, Comment, Application, Host, Inventory
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import OrderedDict


def status_route(request):
    return JsonResponse({'code': 200, 'msg': 'up'})


class MessageViewSet(viewsets.ModelViewSet):
    """show all messages
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MessageSerializer(queryset, many=True)

        return Response([{'id': _.get('id'), 'subject': _.get('subject'), 'timestamp': _.get('timestamp'),
                          'msg': _.get('msg'),
                          'comments': CommentSerializer(Comment.objects.filter(message_id=_.get('id')),
                                                        many=True).data} for
                         _ in serializer.data])


class CommentViewSet(viewsets.ModelViewSet):
    """show all comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)

        return Response([{'id': _.get('id'), 'message': MessageSerializer(
            Message.objects.get(id=_.get('message'))).data.get('msg'), 'message_id': _.get('message'),
                          'comment': _.get('comment'), 'commented_by': _.get('commented_by')} for _ in serializer.data])


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
