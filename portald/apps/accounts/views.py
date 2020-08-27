from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
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
    auth.logout(request)
    return redirect('login')
