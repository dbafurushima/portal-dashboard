from django.shortcuts import render


def login_view(request):
    return render(request, 'auth/sign-in.html')


def register_view(request):
    return render(request, 'auth/sign-out.html')
