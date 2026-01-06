import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.polymerize import Polymerize

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    order_id = post.get('oid')
    amount = post.get('amount')
    amount_type = int(post.get('atype'))
    create_time = post.get('ctime')
    polymerize = Polymerize.objects.add(shop_id, order_id, amount, amount_type, create_time)
    data = Polymerize.objects.encoder(polymerize)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    polymerizes = post.get('p')

    # 批量添加
    for polymerize in polymerizes:
        Polymerize.objects.add(shop_id, polymerize['i'], polymerize['n'], polymerize['sn'])

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Polymerize.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    polymerizes = Polymerize.objects.getList(shop_id, page, num)
    data = Polymerize.objects.encoderList(polymerizes)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
