from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages


@login_required
def clients_view(request):
    armpb = {
        'display_name': 'Armazém Paraíba',
        'img': 'https://via.placeholder.com/80x80'
    }
    clients = [armpb for x in range(20)]
    return render(request, 'pages/management/clients.html',
                  {'clients': clients})


@login_required
def passwords_safe_view(request):
    return render(request, 'pages/management/passwords-safe.html')


@login_required
def register_client(request):
    if request.method == 'POST':
        print(request.POST.keys())
    else:
        return render(request, 'pages/management/clients-register.html')
