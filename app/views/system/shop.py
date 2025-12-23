import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.shop import Shop

@require_POST
def add(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    market_id = int(post.get('mid'))
    name = post.get('name')
    shop = Shop.objects.add(company_id, market_id, name)
    data = Shop.objects.encoder(shop)
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
    name = post.get('name')
    data = Shop.objects.set(pk, name)
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
    data = Shop.objects.delete(pk)
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
    good = Shop.objects.find(pk)
    data = Shop.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    post = json.loads(request.body)
    company_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    goods = Shop.objects.getList(company_id, page, num)
    data = Shop.objects.encoderList(goods)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
