import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.fake import Fake
from app.models.original.user_fake import UserFake
from app.models.system.good import Good

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    orders = UserFake.objects.getAll(user_id, shop_id)

    if orders:
        # 批量添加
        for order in orders:
            order_id = order['order_id']
            procure = order['procure']
            order_status = order['order_status']
            procure_ids = order['procure_ids']
            order_note = order['order_note']

            # 已存在更新订单状态
            find_object = Fake.objects.getById(shop_id, order_id)
            if find_object:
                Fake.objects.set(find_object['id'], procure, order_status, procure_ids, order_note)
            else:
                Fake.objects.add(shop_id, order_id, order['payment'], procure, order_status, order['create_time'], order['good_ids'], procure_ids, order_note)

        # 清空临时数据
        UserFake.objects.deleteAll(user_id, shop_id)

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
    Fake.objects.delete(pk)
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
                    data['good_names'] = data['good_names'] + find_object['short_name'] + ','

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': orders
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
