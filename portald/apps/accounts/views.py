from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice

import datetime


def login_view(request):
    """returns login view if GET or authenticates if POST
    :param request:
    :return:
    """
    request.session['totp'] = False

    if request.method == 'POST' and (request.POST.get('username') and request.POST.get('password')):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('portal-home')
        else:
            messages.error(request, 'usuário ou senha inválido.')
        return redirect('login')
    else:
        return render(request, 'auth/sign-in.html')


def logout_view(request):
    request.session['totp'] = False
    auth.logout(request)
    return redirect('login')


@login_required
def totp_view(request):
    return render(request, 'auth/totp-sign-in.html')


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
    return None


class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)


def totp_check(user: User, token: str) -> bool:
    device = get_user_totp_device(user)

    print(f'device: {device}')
    print(f'verify_token: {device.verify_token(token)}')

    if (device is not None) and (not device.verify_token(token)):

        if not device.confirmed:
            device.confirmed = True
            device.save()

        device.throttle_reset(commit=True)
        return True

    return False


@login_required
def totp_post_view(request):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    user = request.user
    try:
        token = request.POST['token']
    except KeyError:
        token = None

    if token is None:
        return redirect('totp-sign-in')

    if totp_check(user, token):

        request.session['totp'] = True
        request.session['totp_token'] = token

        return redirect('passwords-safe')

    request.session['totp'] = False
    messages.error(request, 'token inválido!')
    return redirect('totp-sign-in')
