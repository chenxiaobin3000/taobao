import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original import order

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def get(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
