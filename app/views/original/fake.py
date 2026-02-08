import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.good_type import GoodType
from app.models.original.fake import Fake
from app.models.system.good import Good

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    orders = post.get('o')
    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }

    # 批量添加
    for order in orders:
        order_id = order['id']
        payment = order['pa']
        procure = order['pr']
        order_status = int(order['st'])
        create_time = order['ct']
        product_name = order['na']
        procure_ids = order['pi']
        order_note = order['no']

        # 已存在更新状态
        find_object = Fake.objects.getById(shop_id, order_id)
        if find_object:
            find_object.procure = procure
            find_object.order_status = order_status
            find_object.procure_ids = procure_ids
            find_object.order_note = order_note
            find_object.save()
        else:
            # 转换商品id
            products = product_name.split(',')
            good_ids = ''
            for product in products:
                good = Good.objects.getByName(shop_id, product)
                if not good:
                    response['code'] = -1
                    response['msg'] = '没有查询到商品:' + product
                    return JsonResponse(response, encoder=MyJSONEncoder)
                if good.good_type != GoodType.GIFT:
                    good_ids = good_ids + good.good_id + '|'
            Fake.objects.add(shop_id, order_id, payment, procure, order_status, create_time, good_ids, procure_ids, order_note)

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Fake.objects.delete(pk)
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
    total = Fake.objects.total(shop_id)
    orders = Fake.objects.getList(shop_id, page, num)

    # 商品id转换商品名称
    if orders:
        for data in orders:
            goods = data['good_ids'].split('|')
            data['good_names'] = ''
            for good in goods:
                find_object = Good.objects.getById(shop_id, good)
                if find_object:
                    data['good_names'] = data['good_names'] + find_object.short_name + ','

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': orders
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
