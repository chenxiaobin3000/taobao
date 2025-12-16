from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.good import Good

@require_POST
def add(request):
    shop_id = request.POST.get('sid')
    good_id = request.POST.get('gid')
    name = request.POST.get('name')
    good = Good.objects.add(shop_id, good_id, name)
    data = Good.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def set(request):
    pk = request.POST.get('id')
    shop_id = request.POST.get('sid')
    good_id = request.POST.get('gid')
    name = request.POST.get('name')
    data = Good.objects.set(pk, shop_id, good_id, name)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def delete(request):
    pk = request.POST.get('id')
    data = Good.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def get(request):
    pk = request.POST.get('id')
    good = Good.objects.find(pk)
    data = Good.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    shop_id = request.POST.get('sid')
    page = int(request.POST.get('page'))
    num = int(request.POST.get('num'))
    goods = Good.objects.getList(shop_id, page, num)
    data = Good.objects.encoderList(goods)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)
