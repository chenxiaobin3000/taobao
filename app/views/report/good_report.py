import json
from datetime import datetime, timedelta
from functools import cmp_to_key
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.good_follow import GoodFollowStatus
from app.models.system.good import Good
from app.models.trunk.order import Order
from app.models.report.good_follow import GoodFollow
from app.models.report.native_promotion_detail import NativePromotionDetail

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    follow = int(post.get('follow'))
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    end_date = datetime.strptime(post.get('edate'), "%Y-%m-%d")
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 生成商品列表
    datas = []
    match follow:
        case GoodFollowStatus.ALL:
            goods = Good.objects.getList(shop_id, 1, 1000)
            if goods:
                for good in goods:
                    datas.append(init_data(good['good_id'], good['short_name']))

        case GoodFollowStatus.HAS_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if temps:
                ids = [temp['good_id'] for temp in temps]
                goods = Good.objects.getListInIds(shop_id, ids)
                if goods:
                    for good in goods:
                        datas.append(init_data(good['good_id'], good['short_name']))

        case GoodFollowStatus.NOT_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if temps:
                ids = [temp['good_id'] for temp in temps]
                goods = Good.objects.getListNotInIds(shop_id, ids)
                if goods:
                    for good in goods:
                        datas.append(init_data(good['good_id'], good['short_name']))

        case _:
            response['code'] = -1
            response['msg'] = '关注类型异常'
            return JsonResponse(response, encoder=MyJSONEncoder)

    # 获取订单数据
    orders= Order.objects.getListByDateRange(shop_id, start_date, end_date)
    if orders:
        # 未发货
        # 已发货
        # 交易成功
        # 交易关闭
        pass

    # 获取推广数据
    promotions= NativePromotionDetail().getSumByDateRange(shop_id, start_date, end_date)
    if promotions:
        for pormotion in promotions:
            for data in datas:
                if data['good_id'] == pormotion['good_id']:
                    data['cost'] = round(pormotion['cost'], 2)
                    data['deal_amount'] = round(pormotion['deal_amount'], 2)
                    data['deal_num'] = round(pormotion['deal_num'], 2)
                    break

    # 按利润排序
    datas = sorted(datas, key = cmp_to_key(lambda a, b: b['cost'] - a['cost']))
    print(datas)
    response['data'] = {
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

def init_data(id, name):
    return {
        'good_id': id,
        'name': name,
        'cost': 0,
        'deal_amount': 0,
        'deal_num': 0
    }
