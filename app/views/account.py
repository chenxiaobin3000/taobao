from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models import account

@require_POST
def register(request):
    response = {}
    response['a'] = account.objects.get(id=1)
    return JsonResponse(response)

@require_POST
def login(request):
    response = {}
    response['code'] = 0
    response['msg'] = '登录成功'
    response['data'] = {}
    response['data']['id'] = 1
    response['data']['token'] = '123456'
    return JsonResponse(response)

@require_POST
def logout(request):
    response = {}
    response['a'] = account.objects.get(id=1)
    return JsonResponse(response)

@require_POST
def setPassword(request):
    response = {}
    response['a'] = account.objects.get(id=1)
    return JsonResponse(response)

@require_POST
def resetPwd(request):
    response = {}
    response['a'] = account.objects.get(id=1)
    return JsonResponse(response)
