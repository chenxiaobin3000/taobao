import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.report.order import Order
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
        datas[start_date.strftime('%Y-%m')] = { 'pending': 0, 'settled': 0, 'refund': 0, 'procure': 0, 'refund_procure': 0, 'transfer': 0, 'deduction': 0, 'promotion': 0, 'fake': 0 }
        month = month + 1
        if month > 12:
            month = 1
            year = year + 1
        start_date = datetime(year, month, 1)

    # 按月生成数据
    pending = 0 # 未完结
    settled = 0 # 已完结
    refund = 0 # 退款
    procure = 0 # 采购
    refund_procure = 0 # 采购退款
    transfer = 0 # 打款
    deduction = 0 # 扣款
    promotion = 0 # 推广
    fake = 0 # 刷单成本

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
            datas[key_month]['refund'] += shipped['refund_customer']
            datas[key_month]['refund'] += shipped['refund_platform']
            datas[key_month]['procure'] += shipped['procure']
            datas[key_month]['refund_procure'] += shipped['refund_procure']
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
            datas[key_month]['refund'] += success['refund_customer']
            datas[key_month]['refund'] += success['refund_platform']
            datas[key_month]['procure'] += success['procure']
            datas[key_month]['refund_procure'] += success['refund_procure']
            datas[key_month]['transfer'] += success['transfer']
            datas[key_month]['deduction'] += success['deduction']
        else:
            response['code'] = -1
            response['msg'] = '数据异常，请联系管理员'
            return JsonResponse(response, encoder=MyJSONEncoder)

    # 已关闭
    closes = Order().groupByMonth(shop_id, OrderStatus.CLOSE)
    for close in closes:
        key_month = success['create_month']
        if key_month in datas:
            datas[key_month]['settled'] += close['payment']
            datas[key_month]['refund'] += close['refund_customer']
            datas[key_month]['refund'] += close['refund_platform']
            datas[key_month]['procure'] += close['procure']
            datas[key_month]['refund_procure'] += close['refund_procure']
            datas[key_month]['transfer'] += close['transfer']
            datas[key_month]['deduction'] += close['deduction']
        else:
            response['code'] = -1
            response['msg'] = '数据异常，请联系管理员'
            return JsonResponse(response, encoder=MyJSONEncoder)

    #     # 推广
    #     promotions = Promotion.objects.getListByDate(shop_id, start)
    #     if promotions:
    #         for temp in promotions:
    #             data['promotion'] += temp['payment']

    #     # 刷单
    #     fake_data = FakeSummary.objects.getByDate(shop_id, start)
    #     if fake_data:
    #         data['fake'] = fake_data['commission'] + fake_data['freight']

    # 统计
    values = datas.values()
    for value in values:
        value['pending'] = round(value['pending'], 2)
        value['settled'] = round(value['settled'], 2)
        value['refund'] = round(value['refund'], 2)
        value['procure'] = round(value['procure'], 2)
        value['refund_procure'] = round(value['refund_procure'], 2)
        value['transfer'] = round(value['transfer'], 2)
        value['deduction'] = round(value['deduction'], 2)
        value['promotion'] = round(value['promotion'], 2)
        value['fake'] = round(value['fake'], 2)

        pending += value['pending']
        settled += value['settled']
        refund += value['refund']
        procure += value['procure']
        refund_procure += value['refund_procure']
        transfer += value['transfer']
        deduction += value['deduction']
        promotion += value['promotion']
        fake += value['fake']

    response['data'] = {
        'pending': round(pending, 2),
        'settled': round(settled, 2),
        'refund': round(refund, 2),
        'procure': round(procure, 2),
        'refund_procure': round(refund_procure, 2),
        'transfer': round(transfer, 2),
        'deduction': round(deduction, 2),
        'promotion': round(promotion, 2),
        'fake': round(fake, 2),
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
