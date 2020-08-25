from django.shortcuts import render
from django.http import JsonResponse


def status_route(request):
    return JsonResponse({'code': 200, 'msg': 'up'})
