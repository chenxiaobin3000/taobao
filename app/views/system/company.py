import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.company import Company

@require_POST
def add(request):
    post = json.loads(request.body)
    name = post.get('name')
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def set(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def delete(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def get(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
