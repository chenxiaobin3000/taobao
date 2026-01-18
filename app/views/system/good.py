import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.good import Good

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    goods = post.get('g')
    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }

    # 批量添加
    for good in goods:
        find_object = Good.objects.getById(shop_id, good['i'])
        if find_object:
            find_object.name = good['n']
            find_object.short_name = good['sn']
            find_object.good_type = good['t']
        else:
            Good.objects.add(shop_id, good['i'], good['n'], good['sn'], good['t'])

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    name = post.get('name')
    short_name = post.get('sname')
    data = Good.objects.set(pk, name, short_name)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Good.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Good.objects.total()
    goods = Good.objects.getList(shop_id, page, num)
    data = Good.objects.encoderList(goods)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
