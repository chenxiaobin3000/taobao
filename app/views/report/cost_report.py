import json
from datetime import datetime, timedelta

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.json_encoder import MyJSONEncoder
from app.models.const.order_status import OrderStatus
from app.models.middle.day_summary import DaySummary
from app.models.trunk.promotion import Promotion
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


def get_shop_window_data(shop_id, start_date, end_date):
    row = empty_row()

    for i in range((end_date - start_date).days + 1):
        create_date = start_date + timedelta(days=i)

        promotions = Promotion.objects.getListByDate(shop_id, create_date)
        if promotions:
            for promotion in promotions:
                row['promotion'] += promotion['payment']

        paid = DaySummary.objects.getByDate(shop_id, create_date, OrderStatus.PAID)
        if paid:
            row['pending'] += paid['payment']

        shipped = DaySummary.objects.getByDate(shop_id, create_date, OrderStatus.SHIPPED)
        if shipped:
            row['pending'] += shipped['payment']
            row['purchase'] += shipped['refund_procure']

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

    for i in range(days):
        create_date = end_date - timedelta(days=i)
        date_key = create_date.strftime('%Y-%m-%d')
        window_start = create_date - timedelta(days=9)
        datas[date_key] = {}
        date_summary = empty_row(date_key)

        for shop_id in shop_ids:
            row = get_shop_window_data(shop_id, window_start, create_date)
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
