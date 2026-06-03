import json
from datetime import datetime, time, timedelta
from decimal import Decimal
from functools import cmp_to_key
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
    date = post.get('date')
    search = post.get('search')
    response = success()

    datas = get_goods(shop_id, follow, search)
    if datas is None:
        return JsonResponse(failed('关注类型异常'), encoder=MyJSONEncoder)

    if date:
        today = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    before_yesterday = today - timedelta(days=2)
    periods = [
        ('yesterday', yesterday, today),
        ('before_yesterday', before_yesterday, yesterday),
        ('three_days', today - timedelta(days=3), today),
        ('seven_days', today - timedelta(days=7), today),
        ('fifteen_days', today - timedelta(days=15), today)
    ]

    for key, start_date, end_date in periods:
        fill_period_data(shop_id, datas, key, start_date, end_date)

    datas = sorted(datas, key=cmp_to_key(lambda a, b: b['three_days']['profit'] - a['three_days']['profit']))
    response['data'] = {
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

def get_goods(shop_id, follow, search=None):
    datas = []
    match follow:
        case GoodFollowStatus.ALL:
            goods = Good.objects.getList(shop_id, 1, 1000)

        case GoodFollowStatus.HAS_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if not temps:
                return datas
            ids = [temp['good_id'] for temp in temps]
            goods = Good.objects.getListInIds(shop_id, ids)

        case GoodFollowStatus.NOT_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if not temps:
                goods = Good.objects.getList(shop_id, 1, 1000)
            else:
                ids = [temp['good_id'] for temp in temps]
                goods = Good.objects.getListNotInIds(shop_id, ids)

        case _:
            return None

    if goods:
        for good in goods:
            if good['good_status'] == GoodStatus.SALE and good['good_type'] == GoodType.NORMAL and match_good(good, search):
                datas.append(init_data(good['good_id'], good['short_name']))
    return datas

def match_good(good, search):
    if not search:
        return True
    keyword = str(search).strip()
    if not keyword:
        return True
    return (
        good['good_id'] == keyword or
        keyword in good['name'] or
        keyword in good['short_name']
    )

def fill_period_data(shop_id, datas, key, start_date, end_date):
    start_time = datetime.combine(start_date, time.min)
    end_time = datetime.combine(end_date, time.min)
    orders = OrderSummary.objects.filter(
        shop_id=shop_id,
        create_time__gte=start_time,
        create_time__lt=end_time
    )
    if orders:
        for order in orders:
            if order.order_status == OrderStatus.PAID or order.order_status == OrderStatus.SHIPPED or order.order_status == OrderStatus.SUCCESS:
                for data in datas:
                    if order.good_ids.find(data['good_id']) != -1:
                        data[key]['payment'] += order.payment
                        data[key]['procure'] += order.procure
                        if len(order.good_ids) == len(data['good_id']) + 1:
                            break
            elif order.order_status == OrderStatus.CLOSE:
                for data in datas:
                    if order.good_ids.find(data['good_id']) != -1:
                        data[key]['close'] += order.payment
                        if len(order.good_ids) == len(data['good_id']) + 1:
                            break

    promotions = NativePromotionDetail().getSumByDateRangeIncludeStart(shop_id, start_date, end_date)
    if promotions:
        for promotion in promotions:
            for data in datas:
                if data['good_id'] == promotion['good_id']:
                    data[key]['cost'] = round(promotion['cost'], 2)
                    data[key]['deal_amount'] = round(promotion['deal_amount'], 2)
                    data[key]['deal_num'] = round(promotion['deal_num'], 2)
                    break

    for data in datas:
        metric = data[key]
        metric['payment'] = round(metric['payment'], 2)
        metric['procure'] = round(metric['procure'], 2)
        metric['close'] = round(metric['close'], 2)
        metric['all'] = round(metric['payment'] + metric['close'], 2)
        metric['profit'] = round(metric['payment'] - Decimal(metric['cost']) - metric['procure'], 2)

def init_data(id, name):
    return {
        'good_id': id,
        'name': name,
        'yesterday': init_metric(),
        'before_yesterday': init_metric(),
        'three_days': init_metric(),
        'seven_days': init_metric(),
        'fifteen_days': init_metric()
    }

def init_metric():
    return {
        'profit': 0,
        'cost': 0,
        'deal_amount': 0,
        'deal_num': 0,
        'all': 0,
        'payment': 0,
        'procure': 0,
        'close': 0
    }
