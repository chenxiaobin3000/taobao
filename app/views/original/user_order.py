import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.good_type import GoodType
from app.models.const.order_status import OrderStatus
from app.models.original.user_order import UserOrder
from app.models.original.user_fake import UserFake
from app.models.system.good import Good
from app.models.system.good_alias import GoodAlias
from app.views.common import failed, success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    orders = post.get('o')
    response = success()

    # 批量添加
    for order in orders:
        order_id = order['id']
        payment = float(order['pa'])
        procure = order['pr']
        order_status = int(order['st'])
        create_time = order['ct']
        procure_ids = order['pi']
        product_name = ''
        if 'na' in order:
            product_name = order['na']
        order_note = ''
        if 'no' in order:
            order_note = order['no']

        # 已存在更新刷单状态
        find_object = UserFake.objects.getById(user_id, shop_id, order_id)
        if find_object:
            UserFake.objects.set(find_object['id'], procure, order_status, procure_ids, order_note)
            continue

        # 已存在更新订单状态
        find_object = UserOrder.objects.getById(user_id, shop_id, order_id)
        if find_object:
            UserOrder.objects.set(find_object['id'], procure, order_status, procure_ids, order_note)
            continue
        
        # 已关闭订单，允许没有商品信息
        if order_status == OrderStatus.CLOSE and len(product_name) == 0:
            UserOrder.objects.add(user_id, shop_id, order_id, payment, procure, order_status, create_time, '', procure_ids, order_note)
        else:
            # 转换商品id
            products = product_name.split(',')
            good_ids = ''
            is_supplement = False
            for product in products:
                # 忽略刷单订单中的赠品和补差价
                if payment <= 6 and len(product) < 10:
                    continue
                # 查询商品表
                good = Good.objects.getByName(shop_id, product)
                if not good:
                    # 查不到就查询别名表
                    good = GoodAlias.objects.getByName(shop_id, product)
                    if good:
                        # 在别名表命中，返回商品表查询
                        good = Good.objects.getById(shop_id, good['good_id'])
                    if not good:
                        return JsonResponse(failed('没有查询到商品:' + order_id + ',' + product), encoder=MyJSONEncoder)
                if good['good_type'] != GoodType.GIFT:
                    good_ids = good_ids + good['good_id'] + '|'
                if good['good_type'] == GoodType.SUPPLEMENT:
                    is_supplement = True
            # 不是补差价，且单价低于6，认定刷单
            if payment <= 6 and not is_supplement:
                UserFake.objects.add(user_id, shop_id, order_id, payment, procure, order_status, create_time, good_ids, procure_ids, order_note)
            else:
                UserOrder.objects.add(user_id, shop_id, order_id, payment, procure, order_status, create_time, good_ids, procure_ids, order_note)

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserOrder.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = request.user_id
    UserOrder.objects.deleteAll(user_id, id)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid') or request.user_id)
    page = int(post.get('page'))
    num = int(post.get('num'))
    search = post.get('search')
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = UserOrder.objects.total(user_id, shop_id, start_date, end_date, search)
    orders = UserOrder.objects.getList(user_id, shop_id, page, num, start_date, end_date, search)

    # 商品id转换商品名称
    if orders:
        for data in orders:
            goods = data['good_ids'].split('|')
            data['good_names'] = ''
            for good in goods:
                find_object = Good.objects.getById(shop_id, good)
                if find_object:
                    data['good_names'] = data['good_names'] + find_object['short_name'] + ','

    response = success({
            'total': total,
            'list': orders
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
