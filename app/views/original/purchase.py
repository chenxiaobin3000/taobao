import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
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
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    order_status = int(post.get('status'))
    Purchase.objects.set(pk, order_status)
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
    data = Purchase.objects.delete(pk)
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
    total = Purchase.objects.total(shop_id)
    purchases = Purchase.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': purchases
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
