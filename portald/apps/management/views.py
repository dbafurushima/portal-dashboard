from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .helper import create_client, create_users, create_default_user
from .models import Client
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import logging


@login_required
def clients_view(request):
    clients = Client.objects.all()
    return render(request, 'pages/management/clients.html',
                  {'clients': clients})


@login_required
def passwords_safe_view(request):
    return render(request, 'pages/management/passwords-safe.html')


@login_required
def register_client(request):
    if request.method == 'POST':

        rt_create = create_client(request.POST)
        if len(rt_create) == 3:
            # incorrect request, doesn't have all fields
            return JsonResponse({'code': 400, 'msg': rt_create[1]})
        else:
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
                # create_default_user(request)
                return JsonResponse({'code': 200,
                                     'msg': 'cadastro da empresa %s realizado com sucesso!' % client.display_name})
            except Exception as err:
                logging.critical(err)
                return JsonResponse({'code': 500, 'msg': 'ocorreu um erro interno no servidor.'})
    else:
        return render(request, 'pages/management/clients-register.html')
