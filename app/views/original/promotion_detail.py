import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.promotion_detail import PromotionDetail

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    polymerizes = post.get('p')

    # 批量添加
    for polymerize in polymerizes:
        promotion_time = polymerize['pt']
        product_id = polymerize['pi']
        show_num = polymerize['sn']
        click_num = polymerize['cn']
        cost = polymerize['co']
        average_cost = polymerize['ac']
        thousand_cost = polymerize['tc']
        deal_amount = polymerize['da']
        deal_num = polymerize['dn']
        deal_cost = polymerize['dc']
        shop_cart = polymerize['sc']
        favorites = polymerize['fa']
        roi = polymerize['roi']
        PromotionDetail.objects.add(shop_id, promotion_time, product_id, show_num, click_num, cost, average_cost, thousand_cost, deal_amount, deal_num, deal_cost, shop_cart, favorites, roi)

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
    data = PromotionDetail.objects.delete(pk)
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
    total = PromotionDetail.objects.total()
    promotions = PromotionDetail.objects.getList(shop_id, page, num)
    data = PromotionDetail.objects.encoderList(promotions)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
