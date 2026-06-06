import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from app.json_encoder import MyJSONEncoder
from app.models.const.omission_order import OmissionOrder
from app.models.const.omission_source import OmissionSource
from app.models.middle.deduction_summary import DeductionSummary
from app.models.middle.omission import Omission
from app.models.trunk.deduction import Deduction
from app.models.trunk.polymerize import Polymerize
from app.models.trunk.order import Order
from app.models.trunk.fake import Fake
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
    if end_date > now_date:
        end_date = now_date
    response = success()

    # 计算开始日期至结束日期的数据
    if end_date <= start_date:
        return JsonResponse(failed('开始日期要早于当前时间'), encoder=MyJSONEncoder)

    # 获取所有扣费和聚合数据
    deductions = Deduction.objects.getAllByDate(shop_id, start_date, end_date)
    polymerizes = Polymerize.objects.getAllByDate(shop_id, start_date, end_date)

    # 清除遗漏数据
    Omission.objects.deleteByDate(shop_id, start_date, end_date)

    # 按本批次数据找出受影响订单
    datas = {}
    amounts = {}
    omissions = []
    order_ids = set()
    for deduction in deductions:
        if deduction['order_id'] != OmissionOrder.VALUE:
            order_ids.add(deduction['order_id'])
    for polymerize in polymerizes:
        if polymerize['order_id'] != OmissionOrder.VALUE:
            order_ids.add(polymerize['order_id'])

    order_id_set = Order.objects.getIds(shop_id, order_ids)
    fake_id_set = Fake.objects.getIds(shop_id, order_ids)
    exists_id_set = order_id_set | fake_id_set

    # 本批次只重建对应时间段的遗漏数据
    if deductions:
        for deduction in deductions:
            oid = deduction['order_id']
            # 处理无订单扣费
            if oid == OmissionOrder.VALUE:
                omissions.append(Omission(shop_id=shop_id, source=OmissionSource.DEDUCTION, order_id=oid, amount=deduction['amount'], create_time=deduction['create_time'], deduction_detail=deduction['deduction_note']))
                continue

            # 校验是否存在关联订单
            if oid not in exists_id_set:
                omissions.append(Omission(shop_id=shop_id, source=OmissionSource.DEDUCTION, order_id=oid, amount=deduction['amount'], create_time=deduction['create_time'], deduction_detail=deduction['deduction_note']))
                continue

    if polymerizes:
        for polymerize in polymerizes:
            oid = polymerize['order_id']
            # 处理无订单聚合
            if oid == OmissionOrder.VALUE:
                omissions.append(Omission(shop_id=shop_id, source=OmissionSource.POLYMERIZE, order_id=oid, amount=polymerize['amount'], create_time=polymerize['create_time'], deduction_detail=polymerize['polymerize_note']))
                continue

            # 校验是否存在关联订单
            if oid not in exists_id_set:
                omissions.append(Omission(shop_id=shop_id, source=OmissionSource.POLYMERIZE, order_id=oid, amount=polymerize['amount'], create_time=polymerize['create_time'], deduction_detail=polymerize['polymerize_note']))
                continue

    # 对受影响订单按完整起始日期重新汇总，避免同一订单跨批次时被局部数据覆盖
    summary_deductions = Deduction.objects.getAllByIds(shop_id, exists_id_set, base_start_date, now_date)
    summary_polymerizes = Polymerize.objects.getAllByIds(shop_id, exists_id_set, base_start_date, now_date)
    if summary_deductions:
        for deduction in summary_deductions:
            oid = deduction['order_id']
            if oid in datas:
                datas[oid] = datas[oid] + '|' + str(deduction['amount_type']) + '-' + str(deduction['amount'])
                amounts[oid] += deduction['amount']
            else:
                datas[oid] = str(deduction['amount_type']) + '-' + str(deduction['amount'])
                amounts[oid] = deduction['amount']

    if summary_polymerizes:
        for polymerize in summary_polymerizes:
            oid = polymerize['order_id']
            if oid in datas:
                datas[oid] = datas[oid] + '|' + str(polymerize['amount_type']) + '-' + str(polymerize['amount'])
                amounts[oid] += polymerize['amount']
            else:
                datas[oid] = str(polymerize['amount_type']) + '-' + str(polymerize['amount'])
                amounts[oid] = polymerize['amount']

    if omissions:
        Omission.objects.bulk_create(omissions, batch_size=1000)

    exists_summary_map = DeductionSummary.objects.getMapByIds(shop_id, datas.keys())
    create_summaries = []
    update_summaries = []
    for key, value in datas.items():
        find_object = exists_summary_map.get(key)
        if find_object:
            if find_object.amount != amounts[key] or find_object.deduction_detail != value:
                find_object.amount = amounts[key]
                find_object.deduction_detail = value
                update_summaries.append(find_object)
        else:
            create_summaries.append(DeductionSummary(shop_id=shop_id, order_id=key, amount=amounts[key], deduction_detail=value))

    if create_summaries:
        DeductionSummary.objects.bulk_create(create_summaries, batch_size=1000)
    if update_summaries:
        DeductionSummary.objects.bulk_update(update_summaries, ['amount', 'deduction_detail'], batch_size=1000)

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
    total = DeductionSummary.objects.total(shop_id, search)
    datas = DeductionSummary.objects.getList(shop_id, page, num, search)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
