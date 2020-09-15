from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializer import NoteSerializer, CommentSerializer, HostSerializer, InventorySerializer, ApplicationSerializer
from .models import Note, Comment, Host, Application
from apps.management.models import Client
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework.decorators import api_view, authentication_classes, permission_classes


def timestamp_to_datetime(ts):
    ts = float(ts) if isinstance(ts, str) else ts
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


class NotesViewSet(viewsets.ModelViewSet):
    """show all notes with comments
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = NoteSerializer(queryset, many=True)

        def comments_by_note(note_id):
            return CommentSerializer(Comment.objects.filter(note_id=note_id), many=True).data

        return Response([{'id': _.get('id'), 'subject': _.get('subject'),
                          'timestamp': timestamp_to_datetime(_.get('timestamp')), 'msg': _.get('msg'),
                          'comments': comments_by_note(_.get('id'))} for
                         _ in serializer.data])


class CommentViewSet(viewsets.ModelViewSet):
    """show all comments with text note
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)

        return Response([{'id': _.get('id'), 'note': NoteSerializer(
            Note.objects.get(id=_.get('note'))).data.get('msg'), 'note_id': _.get('note'),
                          'comment': _.get('comment')} for _ in serializer.data])


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = InventorySerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = InventorySerializer(queryset, many=True)
        data_response = []

        for client in Client.objects.all():
            data_response.append({'client': {'id': client.id, 'company_name': client.company_name},
                                  'hosts': [HostSerializer(host).data for host in Host.objects.filter(enterprise=client)]})

        return Response(data_response)
