import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.refund import Refund
from app.models.original.user_refund import UserRefund
from app.models.original.user_refund_gift import UserRefundGift
from app.models.system.good import Good

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    refunds = UserRefund.objects.getAll(user_id, shop_id)

    if refunds:
    # 批量添加
        for refund in refunds:
            refund_id = refund['refund_id']
            order_id = refund['order_id']
            product_id = refund['product_id']
            actual_pay = refund['actual_pay']
            refund_pay = refund['refund_pay']
            refund_platform = refund['refund_platform']
            refund_type = refund['refund_type']
            refund_status = refund['refund_status']
            apply_time = refund['apply_time']
            timeout_time = refund['timeout_time']
            complete_time = refund['complete_time']

            # 已存在更新状态
            find_object = Refund.objects.getByIdAndTime(shop_id, order_id, refund_id, product_id, apply_time)
            if find_object:
                if find_object['actual_pay'] != actual_pay or find_object['refund_pay'] != refund_pay or find_object['refund_platform'] != refund_platform or find_object['refund_type'] != refund_type or find_object['refund_status'] != refund_status or find_object['timeout_time'] != timeout_time or find_object['complete_time'] != complete_time:
                    Refund.objects.set(find_object['id'], actual_pay, refund_pay, refund_platform, refund_type, refund_status, timeout_time, complete_time)
            else:
                Refund.objects.add(shop_id, refund_id, order_id, product_id, actual_pay, refund_pay, refund_platform, refund_type, refund_status, refund['pay_time'], apply_time, timeout_time, complete_time)

        # 清空临时数据
        UserRefund.objects.deleteAll(user_id, shop_id)
        UserRefundGift.objects.deleteAll(user_id, shop_id)

    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Refund.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Refund.objects.total(shop_id)
    datas = Refund.objects.getList(shop_id, page, num)

    # 商品id转换商品名称
    if datas:
        for refund in datas:
            find_object = Good.objects.getById(shop_id, refund['product_id'])
            if find_object:
                refund['product_name'] = find_object['short_name']

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
