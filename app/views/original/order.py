from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.original import order

@require_POST
def addOrder(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def setOrder(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def delOrder(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getOrder(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getOrderList(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
