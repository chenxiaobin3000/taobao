import json
from datetime import datetime, timedelta

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.json_encoder import MyJSONEncoder
from app.models.const.order_status import OrderStatus
from app.models.report.native_order import NativeOrder
from app.models.report.native_promotion import NativePromotion
from app.views.common import failed, success


def empty_row(create_date=None, shop_id=None):
    return {
        'create_date': create_date,
        'shop_id': shop_id,
        'total_cost': 0,
        'promotion': 0,
        'purchase': 0,
        'pending': 0
    }


def format_row(row):
    row['promotion'] = round(row['promotion'], 1)
    row['purchase'] = round(row['purchase'], 1)
    row['pending'] = round(row['pending'], 1)
    row['total_cost'] = round(row['promotion'] + row['purchase'], 1)
    return row


def add_row(summary, row):
    summary['promotion'] += row['promotion']
    summary['purchase'] += row['purchase']
    summary['pending'] += row['pending']


def build_daily_data(shop_ids, start_date, end_date):
    daily_data = {}
    orders = NativeOrder().groupByDateRange(shop_ids, start_date, end_date)
    for order in orders:
        key = (str(order['shop_id']), order['create_date'])
        row = daily_data.setdefault(key, empty_row(order['create_date'], str(order['shop_id'])))
        if order['order_status'] == OrderStatus.PAID:
            row['pending'] += order['payment']
        elif order['order_status'] == OrderStatus.SHIPPED:
            row['pending'] += order['payment']
            row['purchase'] += order['refund_procure']

    promotions = NativePromotion().groupByDateRange(shop_ids, start_date, end_date)
    for promotion in promotions:
        key = (str(promotion['shop_id']), promotion['create_date'])
        row = daily_data.setdefault(key, empty_row(promotion['create_date'], str(promotion['shop_id'])))
        row['promotion'] += promotion['payment']

    return daily_data


def get_shop_window_data(daily_data, shop_id, start_date, end_date):
    row = empty_row()
    for i in range((end_date - start_date).days + 1):
        key = (str(shop_id), (start_date + timedelta(days=i)).strftime('%Y-%m-%d'))
        day_data = daily_data.get(key)
        if day_data:
            row['promotion'] += day_data['promotion']
            row['purchase'] += day_data['purchase']
            row['pending'] += day_data['pending']
    return format_row(row)


@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_ids = post.get('ids') or []
    if not shop_ids:
        return JsonResponse(failed('至少要选择一个店铺'), encoder=MyJSONEncoder)

    start_date = post.get('sdate')
    end_date = post.get('edate')
    if not start_date or not end_date:
        return JsonResponse(failed('请选择开始日期和结束日期'), encoder=MyJSONEncoder)

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    if start_date > end_date:
        return JsonResponse(failed('开始日期不能晚于结束日期'), encoder=MyJSONEncoder)

    response = success()
    datas = {}
    totals = empty_row()
    days = (end_date - start_date).days + 1
    data_start_date = start_date - timedelta(days=9)
    daily_data = build_daily_data(shop_ids, data_start_date, end_date)

    for i in range(days):
        create_date = end_date - timedelta(days=i)
        date_key = create_date.strftime('%Y-%m-%d')
        window_start = create_date - timedelta(days=9)
        datas[date_key] = {}
        date_summary = empty_row(date_key)

        for shop_id in shop_ids:
            row = get_shop_window_data(daily_data, shop_id, window_start, create_date)
            row['create_date'] = date_key
            row['shop_id'] = str(shop_id)
            datas[date_key][str(shop_id)] = row
            add_row(date_summary, row)

        format_row(date_summary)
        datas[date_key]['summary'] = date_summary
        add_row(totals, date_summary)

    response['data'] = format_row(totals)
    response['data']['list'] = datas
    return JsonResponse(response, encoder=MyJSONEncoder)
