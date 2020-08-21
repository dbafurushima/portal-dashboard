from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .helper import correct_post


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
        if not correct_post(request.POST.keys()):
            messages.error(request, 'incomplete post request, please fill in all necessary fields')
            return redirect('register-client')
        else:
            messages.success(request, 'deu bom parceria')
            return redirect('register-client')
    else:
        return render(request, 'pages/management/clients-register.html')
