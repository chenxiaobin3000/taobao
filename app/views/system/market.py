import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.market import Market

@require_POST
def add(request):
    post = json.loads(request.body)
    name = post.get('name')
    market = Market.objects.add(name)
    data = Market.objects.encoder(market)
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
    data = Market.objects.set(pk, name)
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
    data = Market.objects.delete(pk)
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
    market = Market.objects.find(pk)
    data = Market.objects.encoder(market)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    post = json.loads(request.body)
    page = int(post.get('page'))
    num = int(post.get('num'))
    markets = Market.objects.getList(page, num)
    data = Market.objects.encoderList(markets)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
