import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.good_alias import GoodAlias

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    good_id = post.get('gid')
    name = post.get('name')
    GoodAlias.objects.add(shop_id, good_id, name)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    GoodAlias.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteById(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    good_id = post.get('gid')
    GoodAlias.objects.deleteById(shop_id, good_id)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getById(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    good_id = post.get('gid')
    good = GoodAlias.objects.getById(shop_id, good_id)
    response = {
        'code': 0,
        'msg': 'success',
        'data': good
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getByName(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    good = GoodAlias.objects.getByName(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': good
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = GoodAlias.objects.total(shop_id)
    goods = GoodAlias.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': goods
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
