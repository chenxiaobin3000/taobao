import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.middle.order_summary import OrderSummary
from app.models.middle.day_summary import DaySummary
from app.models.middle.deduction_summary import DeductionSummary
from app.models.trunk.order import Order
from app.models.trunk.fake import Fake
from app.models.trunk.refund import Refund
from app.models.trunk.transfer import Transfer
from app.models.const.order_status import OrderStatus

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    now_date = timezone.now()
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 计算开始日期至今的数据
    duration = now_date - start_date
    days = duration.days
    if days < 1:
        response['code'] = -1
        response['msg'] = '开始日期要早于当前时间'
        return JsonResponse(response, encoder=MyJSONEncoder)

    # 小额打款数据
    transfers = {}
    datas = Transfer.objects.getListByDate(shop_id, start_date)
    if datas:
        for data in datas:
            order_id = data['order_id']
            if order_id in transfers:
                transfers[order_id] += data['amount']
            else:
                transfers[order_id] = data['amount']

    # 生成所有订单数据
    orders = Order.objects.getListByDate(shop_id, start_date)
    if orders:
        for order in orders:
            order_id = order['order_id']
            data = {
                'refund_customer': 0,
                'refund_platform': 0,
                'transfer': 0,
                'deduction': 0,
                'deduction_detail': ''
            }

            # 退款
            refunds = Refund.objects.getById(shop_id, order_id)
            if refunds:
                for refund in refunds:
                    data['refund_customer'] += refund['refund_pay']
                    data['refund_platform'] += refund['refund_platform']

            # 打款
            if order_id in transfers:
                data['transfer'] = transfers[order_id]

            # 扣款
            deduction = DeductionSummary.objects.getById(shop_id, order_id)
            if deduction:
                data['deduction'] = deduction['amount']
                data['deduction_detail'] = deduction['deduction_detail']

            # 采购退款
            refund_procure = 0
            if data['refund_customer'] > 0:
                refund_procure = order['procure']

            # 已经存在，且数据一样就跳过
            find_object = OrderSummary.objects.getById(shop_id, order_id)
            if find_object:
                if find_object['payment'] != order['payment'] or find_object['refund_customer'] != data['refund_customer'] or find_object['refund_platform'] != data['refund_platform'] or find_object['procure'] != order['procure'] or find_object['refund_procure'] != refund_procure or find_object['transfer'] != data['transfer'] or find_object['order_status'] != ['order_status'] or find_object['create_time'] != order['create_time'] or find_object['good_ids'] != order['good_ids'] or find_object['deduction'] != deduction:
                    OrderSummary.objects.set(find_object['id'], order['payment'], data['refund_customer'], data['refund_platform'], order['procure'], refund_procure, data['transfer'], order['order_status'], order['create_time'], order['good_ids'], data['deduction'], data['deduction_detail'])
            else:
                OrderSummary.objects.add(shop_id, order['order_id'], order['payment'], data['refund_customer'], data['refund_platform'], order['procure'], refund_procure, data['transfer'], order['order_status'], order['create_time'], order['good_ids'], data['deduction'], data['deduction_detail'])

    # 按天统计刷单扣款
    fake_deduction = {}
    for i in range(0, days):
        start = start_date + timedelta(days=i)
        end = start_date + timedelta(days=i+1)
        fakes = Fake.objects.getListByDay(shop_id, start, end)
        if fakes:
            temp = 0
            for fake in fakes:
                deduction = DeductionSummary.objects.getById(shop_id, fake['order_id'])
                if deduction:
                    temp += deduction['amount']
            fake_deduction[start.strftime("%Y-%m-%d")] = temp

    # 刷新日报
    DaySummary.objects.deleteByDate(shop_id, start_date)
    for status in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.SUCCESS, OrderStatus.CLOSE]:
        days = OrderSummary.objects.getAll(shop_id, status, start_date, now_date)
        if days:
            for day in days:
                temp = fake_deduction[day['create_date']] if day['create_date'] in fake_deduction else 0
                DaySummary.objects.add(shop_id, day['create_date'], status, day['payment'], day['refund_customer'], day['refund_platform'], day['procure'], day['refund_procure'], day['transfer'], day['deduction'], temp)

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = OrderSummary.objects.total(shop_id)
    fakes = OrderSummary.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': fakes
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
