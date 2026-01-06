import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.purchase import Purchase

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    purchase_id = post.get('pid')
    order_id = post.get('oid')
    payment = post.get('payment')
    freight = post.get('freight')
    total = post.get('total')
    order_status = post.get('status')
    create_time = post.get('ctime')
    product_name = post.get('pn')
    purchase_note = post.get('note')
    purchase = Purchase.objects.add(shop_id, purchase_id, order_id, payment, freight, total, order_status, create_time, product_name, purchase_note)
    data = Purchase.objects.encoder(purchase)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    purchases = post.get('p')

    # 批量添加
    for purchase in purchases:
        Purchase.objects.add(shop_id, purchase['i'], purchase['n'], purchase['sn'])

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
