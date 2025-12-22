import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.good import Good

@require_POST
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('sid'))
    good_id = int(post.get('gid'))
    name = post.get('name')
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
    post = json.loads(request.body)
    pk = int(post.get('id'))
    shop_id = int(post.get('sid'))
    good_id = int(post.get('gid'))
    name = post.get('name')
    data = Good.objects.set(pk, shop_id, good_id, name)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Good.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def get(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
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
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    goods = Good.objects.getList(shop_id, page, num)
    data = Good.objects.encoderList(goods)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)
