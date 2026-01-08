import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.refund import Refund

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    refunds = post.get('r')

    # 批量添加
    for refund in refunds:
        refund_id = refund['uid']
        order_id = refund['oid']
        product_id = refund['pid']
        actual_pay = refund['ap']
        refund_pay = refund['rp']
        refund_type = refund['rt']
        refund_status = refund['rs']
        apply_time = refund['at']
        timeout_time = refund['tt']
        complete_time = refund['ct']

        # 已存在更新状态
        find_object = Refund.objects.getByOIdAndTime(shop_id, order_id, apply_time)
        if find_object:
            if find_object.product_id != product_id or find_object.actual_pay != actual_pay or find_object.refund_pay != refund_pay or find_object.refund_type != refund_type or find_object.refund_status != refund_status or find_object.timeout_time != timeout_time or find_object.complete_time != complete_time:
                find_object.product_id = product_id
                find_object.actual_pay = actual_pay
                find_object.refund_pay = refund_pay
                find_object.refund_type = refund_type
                find_object.refund_status = refund_status
                find_object.timeout_time = timeout_time
                find_object.complete_time = complete_time
                find_object.save()
        else:
            Refund.objects.add(shop_id, refund_id, order_id, product_id, actual_pay, refund_pay, refund_type, refund_status, apply_time, timeout_time, complete_time)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
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
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    refunds = Refund.objects.getList(shop_id, page, num)
    data = Refund.objects.encoderList(refunds)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
