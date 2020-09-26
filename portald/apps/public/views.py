from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def home_view(request):
    return render(request, 'public/home.html')


@login_required
def set_theme_view(request):
    if request.method == 'POST':
        if 'theme' not in request.POST:
            return JsonResponse({'code': 401, 'msg': 'bad request'})
        request.session['theme'] = 'light' if request.POST['theme'] == 'light' else 'dark'
    return JsonResponse({'code': 200, 'msg': 'successful'})
