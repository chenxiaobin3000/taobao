import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_refund_gift import UserRefundGift
from app.models.system.good import Good

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserRefundGift.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = int(post.get('uid'))
    UserRefundGift.objects.deleteAll(user_id, id)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = UserRefundGift.objects.total(user_id, shop_id)
    refunds = UserRefundGift.objects.getList(user_id, shop_id, page, num)

    # 商品id转换商品名称
    if refunds:
        for refund in refunds:
            find_object = Good.objects.getById(shop_id, refund['product_id'])
            if find_object:
                refund['product_name'] = find_object['short_name']

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': refunds
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
