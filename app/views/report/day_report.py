import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.day_summary import DaySummary
from app.models.trunk.promotion import Promotion
from app.models.const.order_status import OrderStatus

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    end_date = datetime.strptime(post.get('edate'), "%Y-%m-%d")
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 计算开始日期至今的数据
    duration = end_date - start_date
    days = duration.days
    if days < 1:
        response['code'] = -1
        response['msg'] = '开始日期要早于结束时间'
        return JsonResponse(response, encoder=MyJSONEncoder)

    # 按天生成数据
    datas = []
    for i in range(0, days):
        start = start_date + timedelta(days=i)
        DaySummary.objects.getByDate(OrderStatus.PAID)
        DaySummary.objects.getByDate(OrderStatus.SHIPPED)
        DaySummary.objects.getByDate(OrderStatus.SUCCESS)
        DaySummary.objects.getByDate(OrderStatus.CLOSE)

        # 推广
        Promotion.objects.getByDate(shop_id, start)

    response['data'] = {
        'pending': 0,
        'settled': 0,
        'refund': 0,
        'procure': 0,
        'refund_procure': 0,
        'transfer': 0,
        'deduction': 0,
        'promotion': 0,
        'fake': 0,
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
