from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models import user

@require_POST
def addUser(request):
    response = {}
    response['a'] = user.objects.get(id=1)
    return JsonResponse(response)

@require_POST
def setUser(request):
    response = {}
    response['a'] = user.objects.get(id=1)
    return JsonResponse(response)

@require_POST
def delUser(request):
    response = {}
    response['a'] = user.objects.get(id=1)
    return JsonResponse(response)

@require_POST
def getUser(request):
    response = {}
    response['code'] = 0
    response['msg'] = 'success'
    response['data'] = {}
    response['data']['user'] = {}
    response['data']['user']['name'] = 'test'
    response['data']['perms'] = [1000,1001]
    response['data']['market'] = [1]
    return JsonResponse(response)

@require_POST
def getUserByPhone(request):
    response = {}
    response['a'] = user.objects.get(id=1)
    return JsonResponse(response)

@require_POST
def getUserList(request):
    response = {}
    response['a'] = user.objects.get(id=1)
    return JsonResponse(response)
