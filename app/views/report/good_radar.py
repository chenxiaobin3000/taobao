import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.good_status import GoodStatus
from app.models.const.good_type import GoodType
from app.models.const.order_status import OrderStatus
from app.models.middle.order_summary import OrderSummary
from app.models.report.native_promotion_detail import NativePromotionDetail
from app.models.system.good import Good
from app.models.system.good_follow import GoodFollow
from app.views.common import failed, success

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    good_id = post.get('good_id')
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    end_date = datetime.strptime(post.get('edate'), "%Y-%m-%d") + timedelta(days=1)

    goods = get_follow_goods(shop_id)
    if not goods:
        response = success({
            'goods': [],
            'list': []
        })
        return JsonResponse(response, encoder=MyJSONEncoder)

    good_ids = [good['good_id'] for good in goods]
    if not good_id:
        good_id = good_ids[0]
    if good_id not in good_ids:
        return JsonResponse(failed('商品异常'), encoder=MyJSONEncoder)

    datas = []
    current = end_date - timedelta(days=1)
    while current >= start_date:
        next_date = current + timedelta(days=1)
        data = init_data(current.strftime("%Y-%m-%d"))
        fill_order_data(shop_id, good_id, current, next_date, data)
        fill_promotion_data(shop_id, good_id, current.date(), next_date.date(), data)
        round_data(data)
        datas.append(data)
        current = current - timedelta(days=1)

    response = success({
        'goods': goods,
        'good_id': good_id,
        'list': datas
    })
    return JsonResponse(response, encoder=MyJSONEncoder)

def get_follow_goods(shop_id):
    follow_ids = GoodFollow.objects.getGoodIds(shop_id)
    if not follow_ids:
        return []
    goods = Good.objects.getListInIds(shop_id, follow_ids)
    if not goods:
        return []
    return [good for good in goods if good['good_status'] == GoodStatus.SALE and good['good_type'] == GoodType.NORMAL]

def fill_order_data(shop_id, good_id, start_date, end_date, data):
    orders = OrderSummary.objects.getListByDateIncludeStart(shop_id, start_date, end_date)
    if not orders:
        return
    for order in orders:
        if order['good_ids'].find(good_id) == -1:
            continue
        if order['order_status'] == OrderStatus.PAID or order['order_status'] == OrderStatus.SHIPPED or order['order_status'] == OrderStatus.SUCCESS:
            data['payment'] += order['payment']
            data['refund'] += order['refund_customer']
            data['refund'] += order['refund_platform']
            data['procure'] += order['procure']
            data['refund_procure'] += order['refund_procure']
            data['deduction'] += order['deduction']
        elif order['order_status'] == OrderStatus.CLOSE:
            if is_refund_after_payment(order):
                data['close'] += order['payment']
                data['close_refund'] += order['refund_customer']
                data['close_refund'] += order['refund_platform']
                data['close_procure'] += order['procure']
                data['close_refund_procure'] += order['refund_procure']
                data['close_deduction'] += order['deduction']
            else:
                data['flash'] += order['payment']
                data['flash_refund'] += order['refund_customer']
                data['flash_refund'] += order['refund_platform']
                data['flash_procure'] += order['procure']
                data['flash_refund_procure'] += order['refund_procure']
                data['flash_deduction'] += order['deduction']

def fill_promotion_data(shop_id, good_id, start_date, end_date, data):
    promotion = NativePromotionDetail().getSumByGoodAndDateRangeIncludeStart(shop_id, good_id, start_date, end_date)
    if promotion:
        data['cost'] = round(promotion['cost'], 2)
        data['deal_amount'] = round(promotion['deal_amount'], 2)
        data['deal_num'] = promotion['deal_num']
        data['shop_cart'] = promotion['shop_cart']
        data['favorites'] = promotion['favorites']

def round_data(data):
    for key in ['payment', 'refund', 'procure', 'refund_procure', 'deduction', 'close', 'close_refund', 'close_procure', 'close_refund_procure', 'close_deduction', 'flash', 'flash_refund', 'flash_procure', 'flash_refund_procure', 'flash_deduction']:
        data[key] = round(data[key], 2)

def init_data(create_date):
    return {
        'create_date': create_date,
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
