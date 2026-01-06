import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.promotion_detail import PromotionDetail

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    polymerizes = post.get('p')

    # 批量添加
    for polymerize in polymerizes:
        promotion_time = polymerize['ptime']
        product_id = polymerize['pid']
        show_num = polymerize['payment']
        click_num = polymerize['freight']
        cost = polymerize['total']
        average_cost = polymerize['status']
        thousand_cost = polymerize['ctime']
        deal_amount = polymerize['pn']
        deal_num = polymerize['note']
        deal_cost = polymerize['note']
        shop_cart = polymerize['note']
        favorites = polymerize['note']
        roi = polymerize['roi']
        PromotionDetail.objects.add(shop_id, promotion_time, product_id, show_num, click_num, cost, average_cost, thousand_cost, deal_amount, deal_num, deal_cost, shop_cart, favorites, roi)

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
