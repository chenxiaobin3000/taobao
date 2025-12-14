from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system import role

@require_POST
def addRole(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def setRole(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def delRole(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getRole(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getRoleList(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
