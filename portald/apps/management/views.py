from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages


@login_required
def passwords_safe_view(request):
    return render(request, 'pages/management/passwords-safe.html')


@login_required
def register_client(request):
    return render(request, 'pages/management/clients-register.html')