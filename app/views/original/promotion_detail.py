import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.promotion_detail import PromotionDetail

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    promotion_time = post.get('ptime')
    product_id = post.get('pid')
    show_num = post.get('payment')
    click_num = post.get('freight')
    cost = post.get('total')
    average_cost = post.get('status')
    thousand_cost = post.get('ctime')
    deal_amount = post.get('pn')
    deal_num = post.get('note')
    deal_cost = post.get('note')
    shop_cart = post.get('note')
    favorites = post.get('note')
    roi = post.get('roi')
    promotion = PromotionDetail.objects.add(shop_id, promotion_time, product_id, show_num, click_num, cost, average_cost, thousand_cost, deal_amount, deal_num, deal_cost, shop_cart, favorites, roi)
    data = PromotionDetail.objects.encoder(promotion)
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
        PromotionDetail.objects.add(shop_id, polymerize['i'], polymerize['n'], polymerize['sn'])

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
    data = PromotionDetail.objects.delete(pk)
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
    promotions = PromotionDetail.objects.getList(shop_id, page, num)
    data = PromotionDetail.objects.encoderList(promotions)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
