from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.company import Company

@require_POST
def add(request):
    name = request.POST.get('name')
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
