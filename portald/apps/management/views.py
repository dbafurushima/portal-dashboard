from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .helper import create_client, create_users, create_default_user, save_password_safe, passwd_from_username
from .models import Client, PasswordSafe
from apps.api.models import Message
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import logging


@login_required
def clients_view(request):
    return render(request, 'pages/management/clients.html',
                  {'clients': Client.objects.all()})


@login_required
def messages_view(request):
    return render(request, 'pages/management/messages.html',
                  {'messages': Message.objects.all()})


@login_required
def passwords_safe_view(request):
    if request.method == 'POST':
        if 'username' not in request.POST.keys():
            return JsonResponse({'code': 400, 'msg': 'incorrect request'})
        pwd = passwd_from_username(request.POST['username'])
        return JsonResponse({'code': 200 if pwd is not None else 404, 'msg': pwd or 'user not found!'})
    clients = Client.objects.all()
    ps_clients = []
    for client in clients:
        cl = {
            'display_name': client.display_name,
            'email': client.user.email,
            'username': client.user.username
        }
        ps_clients.append(cl)
    return render(request, 'pages/management/passwords-safe.html',
                  {'clients': ps_clients})


@login_required
def register_client(request):
    if request.method != 'POST':
        return render(request, 'pages/management/clients-register.html')

    # checks if all required fields exist
    rt_create = create_client(request.POST)

    if len(rt_create) == 3:
        # incorrect request, doesn't have all fields
        return JsonResponse({'code': 400, 'msg': rt_create[1]})
    else:
        # rt_create return False
        if not rt_create[0]:
            return JsonResponse({'code': 400, 'msg': 'o campo "%s" não atende aos requisitos.' % rt_create[1]})

        client = rt_create[1]   # object Client

        if request.FILES['file']:
            file = request.FILES['file']
            if (file.name[-4:] == '.jpg') or (file.name[-4:] == '.png'):
                client.logo = file
                FileSystemStorage().save(file.name, file)

        try:
            client.save()
            # creates all users in the system
            create_users(request.POST)
            password, user = create_default_user(request.POST['email'], client)   # create user for enterprise
            save_password_safe(password, user)    # save password in password safe (table)
            return JsonResponse({'code': 200,
                                 'msg': 'cadastro da empresa %s realizado com sucesso!' % client.display_name})
        except Exception as err:
            logging.critical(err)
            return JsonResponse({'code': 500, 'msg': 'ocorreu um erro interno no servidor.'})

