from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system import permission

@require_POST
def addPermission(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def setPermission(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def delPermission(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getPermission(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getPermissionList(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
