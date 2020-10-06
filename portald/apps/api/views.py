from datetime import datetime
from rest_framework import viewsets
from .serializer import NoteSerializer, CommentSerializer, HostSerializer, InventorySerializer, \
    InstanceSerializer, EnvironmentSerializer, ServiceSerializer
from .models import Note, Comment, Host, Instance, Service, Environment, Inventory
from apps.management.models import Client
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


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


def instances_from_host(host) -> list:
    response = []

    for instance in Instance.objects.filter(host_id=host):
        raw_instance = dict(InstanceSerializer(instance).data)
        service = None if raw_instance.get('service') is None else ServiceSerializer(Service.objects.get(
            id=raw_instance.get('service'))).data

        response.append({
            'id': raw_instance.get('id'),
            'service': service,
            'database': raw_instance.get('database'),
            'private_ip': raw_instance.get('private_ip')
        })

    return response


def host_with_instances_and_service(host):
    new_host = dict(HostSerializer(host).data)
    new_host['instances'] = instances_from_host(host.id)

    return new_host


def hosts_with_instances_and_service():
    return [host_with_instances_and_service(host) for host in Host.objects.all()]


class HostViewSet(viewsets.ModelViewSet):

    queryset = Host.objects.all()
    serializer_class = HostSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = HostSerializer(queryset, many=True)

        return Response(hosts_with_instances_and_service())


class ServiceViewSet(viewsets.ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]


class InstanceViewSet(viewsets.ModelViewSet):

    queryset = Instance.objects.all()
    serializer_class = InstanceSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = InstanceSerializer(queryset, many=True)

        raw_data = []

        for instance in Instance.objects.all():
            new_instance = dict(InstanceSerializer(instance).data)

            new_instance['host'] = HostSerializer(instance.host).data if instance.host else None
            new_instance['service'] = ServiceSerializer(instance.service).data if instance.service else None

            raw_data.append(new_instance)

        return Response(raw_data)


class EnvironmentViewSet(viewsets.ModelViewSet):

    queryset = Host.objects.all()
    serializer_class = EnvironmentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = InventorySerializer(queryset, many=True)

        raw_data = []

        for env in Environment.objects.all():
            new_env = dict(EnvironmentSerializer(env).data)
            new_env['hosts'] = [host_with_instances_and_service(host) for host in Host.objects.filter(environment=env)]
            raw_data.append(new_env)

        return Response(raw_data)


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = InventorySerializer
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = InventorySerializer(queryset, many=True)

        def environment_from_inventory(inv):
            return [(lambda env: {'id': env.get('id'), 'name': env.get('name'),
                                  'hosts': [host_with_instances_and_service(h) for h in Host.objects.filter(
                                      environment_id=env.get('id'))]})(EnvironmentSerializer(env).data)
                    for env in Environment.objects.filter(inventory=inv)]

        raw_data = []
        for inventory in Inventory.objects.all():
            new_inventory = (lambda inv: {'id': inv.get('id'), 'client_id': inv.get('enterprise'),
                                          'client': Client.objects.get(id=inv.get('enterprise')).company_name if
                                          inv.get('enterprise') is not None else None}) \
                (dict(InventorySerializer(inventory).data))
            new_inventory['environments'] = environment_from_inventory(inventory)
            raw_data.append(new_inventory)

        return Response(raw_data)
