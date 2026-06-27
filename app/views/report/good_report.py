import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.good_follow import GoodFollowStatus
from app.models.const.good_status import GoodStatus
from app.models.const.good_type import GoodType
from app.models.const.order_status import OrderStatus
from app.models.system.good import Good
from app.models.middle.order_summary import OrderSummary
from app.models.system.good_follow import GoodFollow
from app.models.report.native_promotion_detail import NativePromotionDetail
from app.views.common import failed, success

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    follow = int(post.get('follow'))
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    end_date = datetime.strptime(post.get('edate'), "%Y-%m-%d")
    response = success()

    # 生成商品列表
    datas = []
    match follow:
        case GoodFollowStatus.ALL:
            goods = Good.objects.getList(shop_id, 1, 1000)
            if goods:
                for good in goods:
                    if good['good_status'] == GoodStatus.SALE and good['good_type'] == GoodType.NORMAL:
                        datas.append(init_data(good['good_id'], good['short_name'], good['origin']))

        case GoodFollowStatus.HAS_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if temps:
                ids = [temp['good_id'] for temp in temps]
                goods = Good.objects.getListInIds(shop_id, ids)
                if goods:
                    for good in goods:
                        if good['good_status'] == GoodStatus.SALE and good['good_type'] == GoodType.NORMAL:
                            datas.append(init_data(good['good_id'], good['short_name'], good['origin']))

        case GoodFollowStatus.NOT_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if temps:
                ids = [temp['good_id'] for temp in temps]
                goods = Good.objects.getListNotInIds(shop_id, ids)
                if goods:
                    for good in goods:
                        if good['good_status'] == GoodStatus.SALE and good['good_type'] == GoodType.NORMAL:
                            datas.append(init_data(good['good_id'], good['short_name'], good['origin']))

        case _:
            return JsonResponse(failed('关注类型异常'), encoder=MyJSONEncoder)

    # 获取订单数据
    orders= OrderSummary.objects.getListByDate(shop_id, start_date, end_date)
    if orders:
        for order in orders:
            if order['order_status'] == OrderStatus.PAID or order['order_status'] == OrderStatus.SHIPPED or order['order_status'] == OrderStatus.SUCCESS:
                for data in datas:
                    if order['good_ids'].find(data['good_id']) != -1:
                        data['payment'] += order['payment']
                        data['refund'] += order['refund_customer']
                        data['refund'] += order['refund_platform']
                        data['procure'] += order['procure']
                        data['refund_procure'] += order['refund_procure']
                        data['deduction'] += order['deduction']
                        if len(order['good_ids']) == len(data['good_id']) + 1:
                            break
            elif order['order_status'] == OrderStatus.CLOSE:
                if is_refund_after_payment(order):
                    for data in datas:
                        if order['good_ids'].find(data['good_id']) != -1:
                            data['close'] += order['payment']
                            data['close_refund'] += order['refund_customer']
                            data['close_refund'] += order['refund_platform']
                            data['close_procure'] += order['procure']
                            data['close_refund_procure'] += order['refund_procure']
                            data['close_deduction'] += order['deduction']
                            if len(order['good_ids']) == len(data['good_id']) + 1:
                                break
                else:
                    for data in datas:
                        if order['good_ids'].find(data['good_id']) != -1:
                            data['flash'] += order['payment']
                            data['flash_refund'] += order['refund_customer']
                            data['flash_refund'] += order['refund_platform']
                            data['flash_procure'] += order['procure']
                            data['flash_refund_procure'] += order['refund_procure']
                            data['flash_deduction'] += order['deduction']
                            if len(order['good_ids']) == len(data['good_id']) + 1:
                                break

    # 获取推广数据
    promotions= NativePromotionDetail().getSumByDateRange(shop_id, start_date, end_date)
    if promotions:
        for pormotion in promotions:
            for data in datas:
                if data['good_id'] == pormotion['good_id']:
                    data['cost'] = round(pormotion['cost'], 2)
                    data['deal_amount'] = round(pormotion['deal_amount'], 2)
                    data['deal_num'] = pormotion['deal_num']
                    data['shop_cart'] = pormotion['shop_cart']
                    data['favorites'] = pormotion['deal_num']
                    break

    for data in datas:
        data['payment'] = round(data['payment'], 2)
        data['refund'] = round(data['refund'], 2)
        data['procure'] = round(data['procure'], 2)
        data['refund_procure'] = round(data['refund_procure'], 2)
        data['deduction'] = round(data['deduction'], 2)
        data['close'] = round(data['close'], 2)
        data['close_refund'] = round(data['close_refund'], 2)
        data['close_procure'] = round(data['close_procure'], 2)
        data['close_refund_procure'] = round(data['close_refund_procure'], 2)
        data['close_deduction'] = round(data['close_deduction'], 2)
        data['flash'] = round(data['flash'], 2)
        data['flash_refund'] = round(data['flash_refund'], 2)
        data['flash_procure'] = round(data['flash_procure'], 2)
        data['flash_refund_procure'] = round(data['flash_refund_procure'], 2)
        data['flash_deduction'] = round(data['flash_deduction'], 2)
    response['data'] = {
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

def init_data(id, name, origin):
    return {
        'good_id': id,
        'origin': origin,
        'name': name,
        'cost': 0,
        'deal_amount': 0,
        'deal_num': 0,
        'shop_cart': 0,
        'favorites': 0,
        'payment': 0,
        'refund': 0,
        'procure': 0,
        'refund_procure': 0,
        'deduction': 0,
        'close': 0,
        'close_refund': 0,
        'close_procure': 0,
        'close_refund_procure': 0,
        'close_deduction': 0,
        'flash': 0,
        'flash_refund': 0,
        'flash_procure': 0,
        'flash_refund_procure': 0,
        'flash_deduction': 0
    }

def is_refund_after_payment(order):
    refund_time = order.get('refund_time')
    if not refund_time:
        return False
    return refund_time - order['create_time'] > timedelta(minutes=30)
