import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from app.json_encoder import MyJSONEncoder
from app.models.const.order_status import OrderStatus
from app.models.middle.order_summary import OrderSummary
from app.models.middle.day_summary import DaySummary
from app.models.middle.deduction_summary import DeductionSummary
from app.models.middle.exist_purchase import ExistPurchase
from app.models.trunk.order import Order
from app.models.trunk.fake import Fake
from app.models.trunk.refund import Refund
from app.models.trunk.transfer import Transfer
from app.models.system.good import Good
from app.views.common import failed, success

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    now_date = timezone.now()
    start_date = parse_date(post.get('sdate'))
    base_start_date = parse_date(post.get('full_sdate')) if post.get('full_sdate') else start_date
    end_date = parse_date(post.get('edate')) if post.get('edate') else now_date
    response = success()

    # 计算开始日期至结束日期的数据
    if end_date <= start_date:
        return JsonResponse(failed('开始日期要早于当前时间'), encoder=MyJSONEncoder)

    # 生成本批次订单数据
    orders = Order.objects.getListByDateRange(shop_id, start_date, end_date)
    if orders:
        order_ids = {order['order_id'] for order in orders}
        transfers = Transfer.objects.getAmountMapByIds(shop_id, order_ids, base_start_date, now_date)
        refunds = Refund.objects.getMapByIds(shop_id, order_ids)
        deductions = DeductionSummary.objects.getMapByIds(shop_id, order_ids)
        exists_orders = OrderSummary.objects.getMapByIds(shop_id, order_ids)

        purchase_ids = set()
        for order in orders:
            procure_ids = order['procure_ids']
            if procure_ids:
                for purchase_id in procure_ids.split('|'):
                    purchase_id = purchase_id.strip()
                    if purchase_id:
                        purchase_ids.add(purchase_id)
        exists_purchase_ids = ExistPurchase.objects.getExistingIds(shop_id, purchase_ids)
        create_purchases = [ExistPurchase(shop_id=shop_id, purchase_id=purchase_id) for purchase_id in purchase_ids if purchase_id not in exists_purchase_ids]
        if create_purchases:
            ExistPurchase.objects.addList(create_purchases)

        create_summaries = []
        update_summaries = []
        for order in orders:
            order_id = order['order_id']
            data = {
                'refund_customer': 0,
                'refund_platform': 0,
                'refund_time': None,
                'transfer': 0,
                'deduction': 0,
                'deduction_detail': ''
            }

            # 退款
            refund = refunds.get(order_id)
            if refund:
                data['refund_customer'] = refund['refund_customer']
                data['refund_platform'] = refund['refund_platform']
                data['refund_time'] = refund['refund_time']

            # 打款
            if order_id in transfers:
                data['transfer'] = transfers[order_id]

            # 扣款
            deduction = deductions.get(order_id)
            if deduction:
                data['deduction'] = deduction.amount
                data['deduction_detail'] = deduction.deduction_detail
            else:
                deduction = { 'amount': 0 }

            # 采购退款
            refund_procure = 0
            if data['refund_customer'] > 0:
                refund_procure = order['procure']

            # 已经存在，且数据一样就跳过
            find_object = exists_orders.get(order_id)
            if find_object:
                if find_object.payment != order['payment'] or find_object.refund_customer != data['refund_customer'] or find_object.refund_platform != data['refund_platform'] or find_object.procure != order['procure'] or find_object.refund_procure != refund_procure or find_object.transfer != data['transfer'] or find_object.order_status != order['order_status'] or find_object.create_time != order['create_time'] or find_object.refund_time != data['refund_time'] or find_object.good_ids != order['good_ids'] or find_object.deduction != data['deduction'] or find_object.deduction_detail != data['deduction_detail']:
                    find_object.payment = order['payment']
                    find_object.refund_customer = data['refund_customer']
                    find_object.refund_platform = data['refund_platform']
                    find_object.procure = order['procure']
                    find_object.refund_procure = refund_procure
                    find_object.transfer = data['transfer']
                    find_object.order_status = order['order_status']
                    find_object.create_time = order['create_time']
                    find_object.refund_time = data['refund_time']
                    find_object.good_ids = order['good_ids']
                    find_object.deduction = data['deduction']
                    find_object.deduction_detail = data['deduction_detail']
                    update_summaries.append(find_object)
            else:
                create_summaries.append(OrderSummary(shop_id=shop_id, order_id=order['order_id'], payment=order['payment'], refund_customer=data['refund_customer'], refund_platform=data['refund_platform'], procure=order['procure'], refund_procure=refund_procure, transfer=data['transfer'], order_status=order['order_status'], create_time=order['create_time'], refund_time=data['refund_time'], good_ids=order['good_ids'], deduction=data['deduction'], deduction_detail=data['deduction_detail']))

        if create_summaries:
            OrderSummary.objects.bulk_create(create_summaries, batch_size=1000)
        if update_summaries:
            OrderSummary.objects.bulk_update(update_summaries, ['payment', 'refund_customer', 'refund_platform', 'procure', 'refund_procure', 'transfer', 'order_status', 'create_time', 'refund_time', 'good_ids', 'deduction', 'deduction_detail'], batch_size=1000)

    # 按天统计刷单扣款
    fake_deduction = {}
    days = (end_date - start_date).days
    fake_order_ids = set()
    fake_days = {}
    for i in range(0, days):
        start = start_date + timedelta(days=i)
        end = start_date + timedelta(days=i+1)
        fakes = Fake.objects.getListByDay(shop_id, start, end)
        if fakes:
            fake_days[start.strftime("%Y-%m-%d")] = fakes
            for fake in fakes:
                fake_order_ids.add(fake['order_id'])
    fake_deductions = DeductionSummary.objects.getMapByIds(shop_id, fake_order_ids)
    for create_date, fakes in fake_days.items():
        temp = 0
        for fake in fakes:
            deduction = fake_deductions.get(fake['order_id'])
            if deduction:
                temp += deduction.amount
        fake_deduction[create_date] = temp

    # 刷新日报
    DaySummary.objects.deleteByDate(shop_id, start_date.date(), end_date.date())
    day_summaries = []
    for status in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.SUCCESS, OrderStatus.CLOSE]:
        days = OrderSummary.objects.getAll(shop_id, status, start_date, now_date)
        if days:
            for day in days:
                day_date = datetime.strptime(day['create_date'], "%Y-%m-%d").date()
                if day_date < start_date.date() or day_date >= end_date.date():
                    continue
                temp = fake_deduction[day['create_date']] if day['create_date'] in fake_deduction else 0
                day_summaries.append(DaySummary(shop_id=shop_id, create_date=day['create_date'], order_status=status, payment=day['payment'], refund_customer=day['refund_customer'], refund_platform=day['refund_platform'], procure=day['procure'], refund_procure=day['refund_procure'], transfer=day['transfer'], deduction=day['deduction'], fake=temp))
    if day_summaries:
        DaySummary.objects.addList(day_summaries)

    return JsonResponse(response, encoder=MyJSONEncoder)

def parse_date(date_text):
    date_value = datetime.strptime(date_text, "%Y-%m-%d")
    if settings.USE_TZ and timezone.is_naive(date_value):
        date_value = timezone.make_aware(date_value)
    return date_value

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    search = post.get('search')
    total = OrderSummary.objects.total(shop_id, search)
    datas = OrderSummary.objects.getList(shop_id, page, num, search)

    # 解析商品名称
    if datas:
        for data in datas:
            goods = data['good_ids']
            if not goods:
                continue
            gids = goods.split('|')
            data['good_names'] = ''
            for gid in gids:
                if gid:
                    good = Good.objects.getById(shop_id, gid)
                    if good:
                        data['good_names'] = data['good_names'] + good['short_name'] + ' | '
            if len(data['good_names']) > 3:
                data['good_names'] = data['good_names'][:-3]

    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
