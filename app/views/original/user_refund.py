import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_refund import UserRefund
from app.models.system.good import Good
from app.models.const.good_type import GoodType

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    refunds = post.get('r')

    # 获取赠品列表
    gifts = []
    goods = Good.objects.getByType(shop_id, GoodType.GIFT)
    for good in goods:
        gifts.append(good.good_id)

    # 批量添加
    for refund in refunds:
        refund_id = refund['uid']
        order_id = refund['oid']
        product_id = refund['pid']
        actual_pay = refund['ap']
        refund_pay = refund['rp']
        refund_platform = refund['rl']
        refund_type = refund['rt']
        refund_status = refund['rs']
        pay_time = refund['pt']
        apply_time = refund['at']
        timeout_time = refund['tt']
        complete_time = refund['ct']

        # 过滤赠品
        if product_id in gifts:
            continue

        # 已存在更新状态
        find_object = UserRefund.objects.getByIdAndTime(user_id, shop_id, order_id, refund_id, product_id, apply_time)
        if find_object:
            if find_object.actual_pay != actual_pay or find_object.refund_pay != refund_pay or find_object.refund_platform != refund_platform or find_object.refund_type != refund_type or find_object.refund_status != refund_status or find_object.timeout_time != timeout_time or find_object.complete_time != complete_time:
                find_object.actual_pay = actual_pay
                find_object.refund_pay = refund_pay
                find_object.refund_platform = refund_platform
                find_object.refund_type = refund_type
                find_object.refund_status = refund_status
                find_object.timeout_time = timeout_time
                find_object.complete_time = complete_time
                find_object.save()
        else:
            UserRefund.objects.add(user_id, shop_id, refund_id, order_id, product_id, actual_pay, refund_pay, refund_platform, refund_type, refund_status, pay_time, apply_time, timeout_time, complete_time)

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
    UserRefund.objects.delete(pk)
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
    user_id = int(post.get('uid'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = UserRefund.objects.total(user_id, shop_id)
    refunds = UserRefund.objects.getList(user_id, shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': refunds
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
