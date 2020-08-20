from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages


@login_required
def list_clients_view(request):
    print(request.session.items())
    return render(request, 'pages/management/clients.html')
