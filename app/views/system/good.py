from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.forms.models import model_to_dict
from app.models.system.good import Good

@require_POST
def add(request):
    shop_id = request.POST.get('sid', 0)
    good_id = request.POST.get('gid', 0)
    name = request.POST.get('name', 0)
    good = Good.objects.add(shop_id, good_id, name)
    data = model_to_dict(good, fields=['id'])
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def set(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    Good.objects.set(1, 'a223', 'hj45')
    return JsonResponse(response)

@require_POST
def delete(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    pk = request.POST.get('id', 0)
    Good.objects.delete(pk)
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
