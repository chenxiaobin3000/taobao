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
        order_id = order['id']
        payment = order['pa']
        procure = order['pr']
        order_status = int(order['st'])
        create_time = order['ct']
        product_name = order['na']
        order_note = order['no']

        # 已存在更新状态
        find_object = Order.objects.getById(shop_id, order_id)
        if find_object:
            find_object.order_status = order_status
            find_object.order_note = order_note
            find_object.save()
        else:
            # 转换商品id
            good_ids = ''
            Order.objects.add(shop_id, order_id, payment, procure, order_status, create_time, good_ids, order_note)

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

    # 商品id转换商品名称

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
