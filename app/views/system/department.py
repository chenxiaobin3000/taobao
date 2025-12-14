from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system import department

@require_POST
def addDepartment(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def setDepartment(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def delDepartment(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getDepartment(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def getDepartmentList(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
