import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.refund import Refund

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    refund_id = post.get('uid')
    order_id = post.get('oid')
    product_id = post.get('pid')
    actual_pay = post.get('ap')
    refund_pay = post.get('rp')
    refund_type = post.get('rt')
    refund_status = post.get('rs')
    apply_time = post.get('at')
    timeout_time = post.get('tt')
    complete_time = post.get('ct')
    transfer = Refund.objects.add(shop_id, refund_id, order_id, product_id, actual_pay, refund_pay, refund_type, refund_status, apply_time, timeout_time, complete_time)
    data = Refund.objects.encoder(transfer)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    refund_status = int(post.get('status'))
    data = Refund.objects.set(pk, refund_status)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

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
    return JsonResponse(response)

@require_POST
@transaction.atomic
def get(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    refund = Refund.objects.find(pk)
    data = Refund.objects.encoder(refund)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

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
    return JsonResponse(response)
