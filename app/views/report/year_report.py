import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.report.order import Order
from app.models.report.fake import Fake
from app.models.report.promotion import Promotion
from app.models.const.order_status import OrderStatus

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    year = 2025
    month = 1
    start_date = datetime(year, month, 1)
    now_date = timezone.now()
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 生成月份列表
    datas = {}
    while start_date < now_date:
        datas[start_date.strftime('%Y-%m')] = { 'pending': 0, 'pending_refund': 0, 'pending_procure': 0, 'pending_refund_procure': 0, 'settled': 0, 'settled_refund': 0, 'settled_procure': 0, 'settled_refund_procure': 0, 'close': 0, 'close_refund': 0, 'close_procure': 0, 'close_refund_procure': 0, 'transfer': 0, 'deduction': 0, 'promotion': 0, 'fake': 0, 'fake_deduction': 0 }
        month = month + 1
        if month > 12:
            month = 1
            year = year + 1
        start_date = datetime(year, month, 1)

    # 按月生成数据
    pending = 0 # 未完结
    pending_refund = 0 # 未完结退款
    pending_procure = 0 # 未完结采购
    pending_refund_procure = 0 # 未完结采购退款
    settled = 0 # 已完结
    settled_refund = 0 # 已完结退款
    settled_procure = 0 # 已完结采购
    settled_refund_procure = 0 # 已完结采购退款
    close = 0 # 关闭
    close_refund = 0 # 关闭退款
    close_procure = 0 # 关闭采购
    close_refund_procure = 0 # 关闭采购退款
    transfer = 0 # 打款
    deduction = 0 # 扣款
    promotion = 0 # 推广
    fake = 0 # 刷单成本
    fake_deduction = 0 # 刷单扣款

    # 待发货
    paids = Order().groupByMonth(shop_id, OrderStatus.PAID)
    for paid in paids:
        key_month = paid['create_month']
        if key_month in datas:
            datas[key_month]['pending'] = paid['payment']
        else:
            response['code'] = -1
            response['msg'] = '数据异常，请联系管理员'
            return JsonResponse(response, encoder=MyJSONEncoder)

    # 已发货
    shippeds = Order().groupByMonth(shop_id, OrderStatus.SHIPPED)
    for shipped in shippeds:
        key_month = shipped['create_month']
        if key_month in datas:
            datas[key_month]['pending'] += shipped['payment']
            datas[key_month]['pending_refund'] += shipped['refund_customer']
            datas[key_month]['pending_refund'] += shipped['refund_platform']
            datas[key_month]['pending_procure'] += shipped['procure']
            datas[key_month]['pending_refund_procure'] += shipped['refund_procure']
        else:
            response['code'] = -1
            response['msg'] = '数据异常，请联系管理员'
            return JsonResponse(response, encoder=MyJSONEncoder)

    # 已结算
    successes = Order().groupByMonth(shop_id, OrderStatus.SUCCESS)
    for success in successes:
        key_month = success['create_month']
        if key_month in datas:
            datas[key_month]['settled'] += success['payment']
            datas[key_month]['settled_refund'] += success['refund_customer']
            datas[key_month]['settled_refund'] += success['refund_platform']
            datas[key_month]['settled_procure'] += success['procure']
            datas[key_month]['settled_refund_procure'] += success['refund_procure']
            datas[key_month]['transfer'] += success['transfer']
            datas[key_month]['deduction'] += success['deduction']
            datas[key_month]['fake_deduction'] += success['fake']
        else:
            response['code'] = -1
            response['msg'] = '数据异常，请联系管理员'
            return JsonResponse(response, encoder=MyJSONEncoder)

    # 已关闭
    closes = Order().groupByMonth(shop_id, OrderStatus.CLOSE)
    for close_data in closes:
        key_month = success['create_month']
        if key_month in datas:
            datas[key_month]['close'] += close_data['payment']
            datas[key_month]['close_refund'] += close_data['refund_customer']
            datas[key_month]['close_refund'] += close_data['refund_platform']
            datas[key_month]['close_procure'] += close_data['procure']
            datas[key_month]['close_refund_procure'] += close_data['refund_procure']
            datas[key_month]['transfer'] += close_data['transfer']
            datas[key_month]['deduction'] += close_data['deduction']
            datas[key_month]['fake_deduction'] += close_data['fake']
        else:
            response['code'] = -1
            response['msg'] = '数据异常，请联系管理员'
            return JsonResponse(response, encoder=MyJSONEncoder)

        # 推广
        promotions = Promotion().groupByMonth(shop_id)
        for temp in promotions:
            key_month = temp['create_month']
            if key_month in datas:
                datas[key_month]['promotion'] = temp['payment']

        # 刷单
        fakes = Fake().groupByMonth(shop_id)
        for temp in fakes:
            key_month = temp['create_month']
            if key_month in datas:
                datas[key_month]['fake'] = temp['commission'] + temp['freight']

    # 统计
    values = datas.values()
    for value in values:
        value['pending'] = round(value['pending'], 2)
        value['pending_refund'] = round(value['pending_refund'], 2)
        value['pending_procure'] = round(value['pending_procure'], 2)
        value['pending_refund_procure'] = round(value['pending_refund_procure'], 2)
        value['settled'] = round(value['settled'], 2)
        value['settled_refund'] = round(value['settled_refund'], 2)
        value['settled_procure'] = round(value['settled_procure'], 2)
        value['settled_refund_procure'] = round(value['settled_refund_procure'], 2)
        value['close'] = round(value['close'], 2)
        value['close_refund'] = round(value['close_refund'], 2)
        value['close_procure'] = round(value['close_procure'], 2)
        value['close_refund_procure'] = round(value['close_refund_procure'], 2)
        value['transfer'] = round(value['transfer'], 2)
        value['deduction'] = round(value['deduction'], 2)
        value['promotion'] = round(value['promotion'], 2)
        value['fake'] = round(value['fake'], 2)
        value['fake_deduction'] = round(value['fake_deduction'], 2)

        pending += value['pending']
        pending_refund += value['pending_refund']
        pending_procure += value['pending_procure']
        pending_refund_procure += value['pending_refund_procure']
        settled += value['settled']
        settled_refund += value['settled_refund']
        settled_procure += value['settled_procure']
        settled_refund_procure += value['settled_refund_procure']
        close += value['close']
        close_refund += value['close_refund']
        close_procure += value['close_procure']
        close_refund_procure += value['close_refund_procure']
        transfer += value['transfer']
        deduction += value['deduction']
        promotion += value['promotion']
        fake += value['fake']
        fake_deduction += value['fake_deduction']

    response['data'] = {
        'pending': round(pending, 2),
        'pending_refund': round(pending_refund, 2),
        'pending_procure': round(pending_procure, 2),
        'pending_refund_procure': round(pending_refund_procure, 2),
        'settled': round(settled, 2),
        'settled_refund': round(settled_refund, 2),
        'settled_procure': round(settled_procure, 2),
        'settled_refund_procure': round(settled_refund_procure, 2),
        'close': round(close, 2),
        'close_refund': round(close_refund, 2),
        'close_procure': round(close_procure, 2),
        'close_refund_procure': round(close_refund_procure, 2),
        'transfer': round(transfer, 2),
        'deduction': round(deduction, 2),
        'promotion': round(promotion, 2),
        'fake': round(fake, 2),
        'fake_deduction': round(fake_deduction, 2),
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
