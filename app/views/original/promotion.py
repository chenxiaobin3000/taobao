import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.promotion import Promotion

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    create_date = post.get('cdate')
    payment = post.get('payment')
    promotion_note = post.get('note')
    promotion = Promotion.objects.add(shop_id, create_date, payment, promotion_note)
    data = Promotion.objects.encoder(promotion)
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
    promotions = post.get('p')

    # 批量添加
    for promotion in promotions:
        Promotion.objects.add(shop_id, promotion['i'], promotion['n'], promotion['sn'])

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
    data = Promotion.objects.delete(pk)
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
    promotions = Promotion.objects.getList(shop_id, page, num)
    data = Promotion.objects.encoderList(promotions)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
