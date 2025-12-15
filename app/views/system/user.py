from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system import user

@require_POST
def add(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def set(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def delete(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def get(request):
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
def getByPhone(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
