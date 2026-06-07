import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.const.order_status import OrderStatus
from app.models.report.native_order import NativeOrder
from app.models.report.native_promotion import NativePromotion
from app.views.common import failed, success

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_ids = post.get('ids')
    response = success()

    deal = 0 # 成交
    deal_tax = 0 # 成交报税
    tax = 0 # 报税
    deduction = 0 # 扣款
    promotion = 0 # 推广

    now_date = timezone.now()
    datas_list = {}
    for shop_id in shop_ids:
        year = 2025
        month = 1
        start_date = datetime(year, month, 1)
        datas = {}
        while start_date < now_date:
            datas[start_date.strftime('%Y-%m')] = {
                'deal': 0,
                'deal_tax': 0,
                'tax': 0,
                'deduction': 0,
                'promotion': 0
            }
            month = month + 1
            if month > 12:
                month = 1
                year = year + 1
            start_date = datetime(year, month, 1)
        datas_list[shop_id] = datas

        successes = NativeOrder().groupByMonth(shop_id, OrderStatus.SUCCESS)
        for success_data in successes:
            key_month = success_data['create_month']
            if key_month in datas:
                datas[key_month]['deal'] += success_data['payment']
                datas[key_month]['deduction'] += success_data['deduction']
            else:
                return JsonResponse(failed('数据异常，请联系管理员'), encoder=MyJSONEncoder)

        promotions = NativePromotion().groupByMonth(shop_id)
        for temp in promotions:
            key_month = temp['create_month']
            if key_month in datas:
                datas[key_month]['promotion'] = temp['payment']

        for value in datas.values():
            value['deal'] = round(value['deal'], 1)
            value['deduction'] = round(value['deduction'], 1)
            value['promotion'] = round(value['promotion'], 1)
            value['deal_tax'] = round(value['deal'] * 0.06, 1)
            value['tax'] = round((value['deal'] - value['promotion']) * 0.06, 1)

            deal += value['deal']
            deal_tax += value['deal_tax']
            tax += value['tax']
            deduction += value['deduction']
            promotion += value['promotion']

    year = 2025
    month = 1
    start_date = datetime(year, month, 1)
    datas = {}
    while start_date < now_date:
        key_month = start_date.strftime('%Y-%m')
        datas[key_month] = {}
        for shop_id in shop_ids:
            datas[key_month][shop_id] = datas_list[shop_id][key_month]
        month = month + 1
        if month > 12:
           month = 1
           year = year + 1
        start_date = datetime(year, month, 1)

    response['data'] = {
        'deal': round(deal, 1),
        'deal_tax': round(deal_tax, 1),
        'tax': round(tax, 1),
        'deduction': round(deduction, 1),
        'promotion': round(promotion, 1),
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
