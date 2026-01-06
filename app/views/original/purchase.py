import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.purchase import Purchase

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    purchases = post.get('p')

    # 批量添加
    for purchase in purchases:
        purchase_id = purchase['pid']
        order_id = purchase['oid']
        payment = purchase['payment']
        freight = purchase['freight']
        total = purchase['total']
        order_status = purchase['status']
        create_time = purchase['ctime']
        product_name = purchase['pn']
        purchase_note = purchase['note']
        Purchase.objects.add(shop_id, purchase_id, order_id, payment, freight, total, order_status, create_time, product_name, purchase_note)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    order_status = int(post.get('status'))
    data = Purchase.objects.set(pk, order_status)
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
    data = Purchase.objects.delete(pk)
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
    purchases = Purchase.objects.getList(shop_id, page, num)
    data = Purchase.objects.encoderList(purchases)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
