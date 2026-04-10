import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.promotion_detail import PromotionDetail
from app.models.original.user_promotion_detail import UserPromotionDetail
from app.models.system.good import Good

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    polymerizes = UserPromotionDetail.objects.getAll(user_id, shop_id)

    if polymerizes:
        # 批量添加
        for polymerize in polymerizes:
            promotion_date = polymerize['promotion_date']
            good_id = polymerize['good_id']
            if PromotionDetail.objects.getByIdAndDate(shop_id, promotion_date, good_id):
                continue
            PromotionDetail.objects.add(shop_id, promotion_date, good_id, polymerize['show_num'], polymerize['click_num'], polymerize['click_rate'], polymerize['cost'], polymerize['average_cost'], polymerize['thousand_cost'], polymerize['deal_amount'], polymerize['deal_num'], polymerize['deal_cost'], polymerize['shop_cart'], polymerize['favorites'], polymerize['roi'])

        # 清空临时数据
        UserPromotionDetail.objects.deleteAll(user_id, shop_id)

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
    PromotionDetail.objects.delete(pk)
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
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = PromotionDetail.objects.total(shop_id)
    datas = PromotionDetail.objects.getList(shop_id, page, num)

    # 商品信息
    if datas:
        for data in datas:
            good = Good.objects.getById(shop_id, data['good_id'])
            if good:
                data['good_name'] = good['short_name']
            else:
                data['good_name'] = data['good_id']

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
