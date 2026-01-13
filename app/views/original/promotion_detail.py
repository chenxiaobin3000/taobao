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
    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }

    # 批量添加
    for polymerize in polymerizes:
        promotion_date = polymerize['pd']
        good_id = polymerize['id']
        show_num = int(polymerize['sn'])
        click_num = int(polymerize['cn'])
        cost = polymerize['co']
        average_cost = polymerize['ac']
        thousand_cost = polymerize['tc']
        deal_amount = polymerize['da']
        deal_num = int(polymerize['dn'])
        deal_cost = polymerize['dc']
        shop_cart = int(polymerize['sc'])
        favorites = int(polymerize['fa'])
        roi = polymerize['roi']

        # 不存在就插入
        find_object = PromotionDetail.objects.getByIdAndDate(shop_id, promotion_date, good_id)
        if not find_object:
            PromotionDetail.objects.add(shop_id, promotion_date, good_id, show_num, click_num, cost, average_cost, thousand_cost, deal_amount, deal_num, deal_cost, shop_cart, favorites, roi)

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
    datas = PromotionDetail.objects.encoderList(promotions)

    # 商品信息
    for data in datas:
        good = Good.objects.getById(shop_id, data.good_id)
        data['good_name'] = good.short_name

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
