import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.day_summary import DaySummary
from app.models.middle.fake_summary import FakeSummary
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
    pending = 0 # 未完结
    settled = 0 # 已完结
    refund = 0 # 退款
    close = 0 # 关闭
    close_refund = 0 # 关闭退款
    procure = 0 # 采购
    refund_procure = 0 # 采购退款
    transfer = 0 # 打款
    deduction = 0 # 扣款
    promotion = 0 # 推广
    fake = 0 # 刷单成本
    fake_deduction = 0 # 刷单扣款
    datas = []
    for i in range(0, days):
        start = start_date + timedelta(days=i)
        data = { 'create_date': start.strftime('%Y-%m-%d'), 'pending': 0, 'settled': 0, 'refund': 0, 'close': 0, 'close_refund': 0, 'procure': 0, 'refund_procure': 0, 'transfer': 0, 'deduction': 0, 'promotion': 0, 'fake': 0, 'fake_deduction': 0 }

        # 待发货
        paid = DaySummary.objects.getByDate(shop_id, start, OrderStatus.PAID)
        if paid:
            data['pending'] += paid['payment']

        # 已发货
        shipped = DaySummary.objects.getByDate(shop_id, start, OrderStatus.SHIPPED)
        if shipped:
            data['pending'] += shipped['payment']
            data['refund'] += shipped['refund_customer']
            data['refund'] += shipped['refund_platform']
            data['procure'] += shipped['procure']
            data['refund_procure'] += shipped['refund_procure']

        # 已结算
        success = DaySummary.objects.getByDate(shop_id, start, OrderStatus.SUCCESS)
        if success:
            data['settled'] += success['payment']
            data['refund'] += success['refund_customer']
            data['refund'] += success['refund_platform']
            data['procure'] += success['procure']
            data['refund_procure'] += success['refund_procure']
            data['transfer'] += success['transfer']
            data['deduction'] += success['deduction']
            data['fake_deduction'] += success['fake']

        # 已关闭
        close_data = DaySummary.objects.getByDate(shop_id, start, OrderStatus.CLOSE)
        if close_data:
            data['close'] += close_data['payment']
            data['close_refund'] += close_data['refund_customer']
            data['close_refund'] += close_data['refund_platform']
            data['procure'] += close_data['procure']
            data['refund_procure'] += close_data['refund_procure']
            data['transfer'] += close_data['transfer']
            data['deduction'] += close_data['deduction']
            data['fake_deduction'] += close_data['fake']

        # 推广
        promotions = Promotion.objects.getListByDate(shop_id, start)
        if promotions:
            for temp in promotions:
                data['promotion'] += temp['payment']

        # 刷单
        fake_data = FakeSummary.objects.getByDate(shop_id, start)
        if fake_data:
            data['fake'] = fake_data['commission'] + fake_data['freight']

        # 统计
        pending += data['pending']
        settled += data['settled']
        refund += data['refund']
        close += data['close']
        close_refund += data['close_refund']
        procure += data['procure']
        refund_procure += data['refund_procure']
        transfer += data['transfer']
        deduction += data['deduction']
        promotion += data['promotion']
        fake += data['fake']
        fake_deduction += data['fake_deduction']
        datas.insert(0, data)

    response['data'] = {
        'pending': pending,
        'settled': settled,
        'refund': refund,
        'close': close,
        'close_refund': close_refund,
        'procure': procure,
        'refund_procure': refund_procure,
        'transfer': transfer,
        'deduction': deduction,
        'promotion': promotion,
        'fake': fake,
        'fake_deduction': fake_deduction,
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
