import requests
import logging
import json
import pprint
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.db import (DatabaseError, DataError, InternalError, IntegrityError)

from .helper import (_create_client_from_post, _create_users, _create_default_user,
                     _save_password_safe, passwd_from_username,
                     __create_user)
from apps.accounts.views import totp_check
from .models import Client, EnterpriseUser
from apps.api.models import Environment, Inventory, Host, Instance, Service
from apps.api.serializer import (InventorySerializer, EnvironmentSerializer, HostSerializer, InstanceSerializer,
                                 ServiceSerializer)
from apps.errors import Errors


def permission_check(user: User):
    return user.is_superuser


@login_required
@user_passes_test(permission_check)
def proxy_api_view(request):
    if request.method == 'GET':
        return JsonResponse({'proxy': 'running'})

    payload_for_api = dict(request.POST)
    for item in payload_for_api:
        payload_for_api[item] = payload_for_api[item][0]

    route = payload_for_api.get('route')
    payload_for_api.pop('route')
    payload_for_api.pop('csrfmiddlewaretoken')

    print(payload_for_api)

    response_api = json.loads(requests.post(
        f'http://{request.headers.get("Host")}{route}', payload_for_api,
        headers={'Authorization': f'Token {settings.USER_API_KEY}'}).text)

    print(response_api)

    if response_api.get('id'):
        messages.success(request,
                         f'Item com id "{response_api.get("id")}" criado com sucesso!')
    else:
        messages.error(request, response_api)

    return redirect('inventory')


@login_required
@user_passes_test(permission_check)
def inventory_view(request):
    pp = pprint.PrettyPrinter(indent=2, compact=False, width=41, sort_dicts=False)

    if request.method == 'GET':
        clients = Client.objects.all()
        return render(request, 'pages/management/inventory.html',
                      {'data': {'clients': clients,
                                'inventories': Inventory.objects.all(),
                                'envs': Environment.objects.all(),
                                'services': Service.objects.all(),
                                'hosts': Host.objects.all()
                                }
                     })

    def inventory_by_client_id(cid):
        index = (n for n in range(1, 100))

        raw_inventories = [dict(InventorySerializer(inventory).data)
                           for inventory in Inventory.objects.filter(enterprise_id=int(cid))]

        inventories = [(lambda inv: {'id': next(index), 'name': 'Inventário', 'type': 'Root', 'uid': inv.get('id'),
                                     'description': Client.objects.get(id=inv.get('id')).company_name})(inventory) for
                       inventory in raw_inventories]

        raw_environments = [dict(EnvironmentSerializer(env).data) for env in Environment.objects.all()]

        environments = [(lambda e: {'id': next(index), 'name': 'Ambiente', 'description': env.get('name'),
                                    'type': 'Type', 'uid': env.get('inventory'), 'uid2': env.get('id')})(env)
                        for env in raw_environments]

        raw_hosts = [dict(HostSerializer(host).data) for host in Host.objects.all()]

        hosts = [(lambda h: {'id': next(index), 'name': 'Máquina', 'description': h.get('hostname'),
                             'type': 'Family', 'uid': h.get('environment'), 'uid2': h.get('id')})(host)
                 for host in raw_hosts]

        raw_instances = [dict(InstanceSerializer(instance).data) for instance in Instance.objects.all()]

        def service_name_by_id(sid: int) -> str:
            if sid is None:
                return 'None'
            try:
                name = '/'+Service.objects.get(id=sid).name
            except Exception as err:
                name = ''
            return name

        instances = [
            (lambda i: {'id': next(index), 'name': 'Instância',
                        'description': i.get('database')+service_name_by_id(i.get('service')), 'type': 'Family',
                        'uid': i.get('host'), 'uid2': i.get('service')})(instance)
            for instance in raw_instances]

        raw_services = [dict(ServiceSerializer(service).data) for service in Service.objects.all()]

        """
        services = [(lambda s: {'id': next(index), 'name': 'Serviço', 'description': s.get('name'),
                                'type': 'Family', 'uid': s.get('id')})(service)
                    for service in raw_services]
        """

        if instances:
            for instance in instances:
                pass
                """
                instance['children'] = [service if service.get('uid') == instance.get('uid2')
                                        else None for service in services]
                while None in instance['children']:
                    instance['children'].remove(None)
                """

        if hosts:
            for host in hosts:
                host['children'] = [instance if instance.get('uid') == host.get('uid2') else None for instance in
                                    instances]
                while None in host['children']:
                    host['children'].remove(None)

        if environments:
            for env in environments:
                env['children'] = [host if host.get('uid') == env.get('uid2') else None for host in hosts]
                while None in env['children']:
                    env['children'].remove(None)

        if inventories:
            for inventory in inventories:
                inventory['children'] = [env if env.get('uid') == inventory.get('uid') else None for env in
                                         environments]
                while None in inventory['children']:
                    inventory['children'].remove(None)

        inventories = inventories[0] if len(inventories) > 0 else inventories

        pp.pprint(inventories)

        return {'data': inventories}

    client_id = request.POST['client_id'] or 0

    return JsonResponse(inventory_by_client_id(client_id))


@login_required
@user_passes_test(permission_check)
def clients_view(request):
    return render(request, 'pages/management/clients.html',
                  {'clients': Client.objects.all()})


@login_required
@user_passes_test(permission_check)
def todolist_view(request):
    return render(request, 'pages/management/todolist.html',
                  {'notes': json.loads(requests.get('http://localhost:8000/api/message/',
                                                    headers={'Authorization': f'Token {settings.USER_API_KEY}'}).text)}
                  )


@login_required
@user_passes_test(permission_check)
def kanban_view(request):
    return render(request, 'pages/management/kanban.html',
                  {'notes': json.loads(requests.get(f'http://{request.headers.get("host")}/api/note/',
                                                    headers={'Authorization': f'Token {settings.USER_API_KEY}'}).text)}
                  )


@login_required
@user_passes_test(permission_check)
def passwords_safe_view(request):

    def verify_expire(dt_expire: str) -> bool:
        dt_now = datetime.datetime.now()
        dt_stftime = dt_now.strftime('%H-%M-%S')

        nh, nm, ns = dt_stftime.split('-')
        eh, em, es = dt_expire.split('-')

        if int(nh) > int(eh):
            return False
        if int(nm) > int(em):
            return False

        return True

    if (not request.session.get('totp')) or (not totp_check(request.user, request.session.get('token'))):
        return redirect('totp-sign-in')

    if not verify_expire(request.session.get('totp_expire')):
        return redirect('totp-sign-in')

    if request.method == 'POST':
        if 'add' and 'username' and 'enterprise' and 'passwd' in request.POST.keys():
            client: Client = Client.objects.get(id=int(request.POST['enterprise']))
            username = request.POST['username']
            email = username + '@' + client.user.email.split('@')[-1]
            __create_user(username, email, request.POST['passwd'], client)

            return JsonResponse({'code': 200, 'msg': 'user created!'})

        if 'username' not in request.POST.keys():
            return JsonResponse({'code': 400, 'msg': 'incorrect request'})

        pwd = passwd_from_username(request.POST['username'])
        return JsonResponse({'code': 200 if pwd is not None else 404, 'msg': pwd or 'user not found!'})

    return render(request, 'pages/management/passwords-safe.html',
                  {'data': {'users': [{'id': eu.enterprise.id, 'username': eu.user.username, 'email': eu.user.email,
                                       'display_name': eu.enterprise.display_name,
                                       'username2': eu.user.username.replace('.', '-')} for eu in
                                      EnterpriseUser.objects.all()],
                            'clients': [{'id': client.id, 'display_name': client.display_name} for client in
                                        Client.objects.all()]}}
                  )


@login_required
@user_passes_test(permission_check)
def register_client(request):

    def __save_logo(file, client: Client) -> None:
        if (file.name[-4:] == '.jpg') or (file.name[-4:] == '.png'):
            client.logo = file
            FileSystemStorage().save(file.name, file)

    if request.method != 'POST':
        return render(request, 'pages/management/clients-register.html')

    itworked, message, client = _create_client_from_post(request.POST)

    if not itworked:
        return JsonResponse(
            {
                'code': 400,
                'msg': message
            }
        )

    if request.FILES:
        __save_logo(request.FILES['file'], client)

    try:
        client.save()
        _create_users(request.POST, client)
        password, user = _create_default_user(request.POST['email'], client)  # create user for enterprise
        _save_password_safe(password, user)  # save password in password safe (table)

        try:
            Inventory(enterprise=client).save()
        except (DatabaseError, DataError, InternalError, IntegrityError):
            logging.critical('%s -> %s' % Errors.name_and_error(Errors.DATABASE_UNKNOWN_INTERNAL_ERROR))

    except Exception as err:
        logging.critical(err)

        return JsonResponse(
            {
                'code': 500,
                'msg': '%s -> %s' % Errors.name_and_error(Errors.HTTP_500_INTERNAL_ERROR)
            })
    else:
        return JsonResponse(
            {
                'code': 200,
                'msg': 'Cadastro da empresa "%s" realizado com sucesso!' % client.display_name
            })
