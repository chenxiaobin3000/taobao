import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.order import Order

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    orders = post.get('o')

    # 批量添加
    for order in orders:
        order_id = order['oid']
        payment = order['payment']
        actual_pay = order['ap']
        procure_pay = order['pp']
        order_status = int(order['status'])
        create_time = order['ctime']
        product_name = order['name']
        order_note = order['note']
        Order.objects.add(shop_id, order_id, payment, actual_pay, procure_pay, order_status, create_time, product_name, order_note)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    procure_pay = int(post.get('pay'))
    order_status = int(post.get('status'))
    order_note = int(post.get('note'))
    data = Order.objects.set(pk, procure_pay, order_status, order_note)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Order.objects.delete(pk)
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
    total = Order.objects.total()
    orders = Order.objects.getList(shop_id, page, num)
    data = Order.objects.encoderList(orders)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
