from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system import user

@require_POST
def addUser(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def setUser(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def delUser(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getUser(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'user': {
                'name': 'test',
                'phone': '123'
            },
            'depart': {},
            'perms': [1000,1001,1002,1003],
            'market': [1]
        }
    }
    return JsonResponse(response)

@require_POST
def getUserByPhone(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getUserList(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
