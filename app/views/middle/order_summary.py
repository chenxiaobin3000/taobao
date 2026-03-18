import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.middle.order_summary import OrderSummary
from app.models.middle.deduction_summary import DeductionSummary
from app.models.trunk.order import Order
from app.models.trunk.refund import Refund
from app.models.trunk.transfer import Transfer

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
    datas = Transfer.objects.getAll(shop_id)
    if datas:
        for data in datas:
            order_id = data['order_id']
            if order_id in transfers:
                transfers[order_id] += data['amount']
            else:
                transfers[order_id] = data['amount']

    # 生成所有订单数据
    orders = Order.objects.getAll(shop_id, start_date)
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

            # 已经存在，且数据一样就跳过
            find_object = OrderSummary.objects.getById(shop_id, order_id)
            if find_object:
                if find_object['payment'] != order['payment'] or find_object['refund_customer'] != data['refund_customer'] or find_object['refund_platform'] != data['refund_platform'] or find_object['procure'] != order['procure'] or find_object['refund_procure'] != order['procure'] or find_object['transfer'] != data['transfer'] or find_object['order_status'] != ['order_status'] or find_object['create_time'] != order['create_time'] or find_object['good_ids'] != order['good_ids'] or find_object['deduction'] != deduction:
                    OrderSummary.objects.set(find_object['id'], order['payment'], data['refund_customer'], data['refund_platform'], order['procure'], order['procure'], data['transfer'], order['order_status'], order['create_time'], order['good_ids'], data['deduction'], data['deduction_detail'])
            else:
                OrderSummary.objects.add(shop_id, order['order_id'], order['payment'], data['refund_customer'], data['refund_platform'], order['procure'], order['procure'], data['transfer'], order['order_status'], order['create_time'], order['good_ids'], data['deduction'], data['deduction_detail'])

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
