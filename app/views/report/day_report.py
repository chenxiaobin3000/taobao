import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.order_status import OrderStatus
from app.models.middle.day_summary import DaySummary
from app.models.middle.fake_summary import FakeSummary
from app.models.trunk.promotion import Promotion

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
    datas = []
    for i in range(0, days):
        start = start_date + timedelta(days=i)
        data = { 'create_date': start.strftime('%Y-%m-%d'), 'pending': 0, 'pending_refund': 0, 'pending_procure': 0, 'pending_refund_procure': 0, 'settled': 0, 'settled_refund': 0, 'settled_procure': 0, 'settled_refund_procure': 0, 'close': 0, 'close_refund': 0, 'close_procure': 0, 'close_refund_procure': 0, 'transfer': 0, 'deduction': 0, 'promotion': 0, 'fake': 0, 'fake_deduction': 0 }

        # 待发货
        paid = DaySummary.objects.getByDate(shop_id, start, OrderStatus.PAID)
        if paid:
            data['pending'] += paid['payment']

        # 已发货
        shipped = DaySummary.objects.getByDate(shop_id, start, OrderStatus.SHIPPED)
        if shipped:
            data['pending'] += shipped['payment']
            data['pending_refund'] += shipped['refund_customer']
            data['pending_refund'] += shipped['refund_platform']
            data['pending_procure'] += shipped['procure']
            data['pending_refund_procure'] += shipped['refund_procure']

        # 已结算
        success = DaySummary.objects.getByDate(shop_id, start, OrderStatus.SUCCESS)
        if success:
            data['settled'] += success['payment']
            data['settled_refund'] += success['refund_customer']
            data['settled_refund'] += success['refund_platform']
            data['settled_procure'] += success['procure']
            data['settled_refund_procure'] += success['refund_procure']
            data['transfer'] += success['transfer']
            data['deduction'] += success['deduction']
            data['fake_deduction'] += success['fake']

        # 已关闭
        close_data = DaySummary.objects.getByDate(shop_id, start, OrderStatus.CLOSE)
        if close_data:
            data['close'] += close_data['payment']
            data['close_refund'] += close_data['refund_customer']
            data['close_refund'] += close_data['refund_platform']
            data['close_procure'] += close_data['procure']
            data['close_refund_procure'] += close_data['refund_procure']
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
        pending_refund += data['pending_refund']
        pending_procure += data['pending_procure']
        pending_refund_procure += data['pending_refund_procure']
        settled += data['settled']
        settled_refund += data['settled_refund']
        settled_procure += data['settled_procure']
        settled_refund_procure += data['settled_refund_procure']
        close += data['close']
        close_refund += data['close_refund']
        close_procure += data['close_procure']
        close_refund_procure += data['close_refund_procure']
        transfer += data['transfer']
        deduction += data['deduction']
        promotion += data['promotion']
        fake += data['fake']
        fake_deduction += data['fake_deduction']
        datas.insert(0, data)

    response['data'] = {
        'pending': pending,
        'pending_refund': pending_refund,
        'pending_procure': pending_procure,
        'pending_refund_procure': pending_refund_procure,
        'settled': settled,
        'settled_refund': settled_refund,
        'settled_procure': settled_procure,
        'settled_refund_procure': settled_refund_procure,
        'close': close,
        'close_refund': close_refund,
        'close_procure': close_procure,
        'close_refund_procure': close_refund_procure,
        'transfer': transfer,
        'deduction': deduction,
        'promotion': promotion,
        'fake': fake,
        'fake_deduction': fake_deduction,
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
