import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.promotion import Promotion

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    promotions = post.get('p')

    # 批量添加
    for promotion in promotions:
        create_date = promotion['d']
        payment = promotion['p']
        promotion_type = promotion['t']
        promotion_note = promotion['n']
        if Promotion.objects.getByCDate(shop_id, create_date, promotion_type):
            continue
        Promotion.objects.add(shop_id, create_date, payment, promotion_type, promotion_note)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

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
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Promotion.objects.total()
    promotions = Promotion.objects.getList(shop_id, page, num)
    data = Promotion.objects.encoderList(promotions)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
