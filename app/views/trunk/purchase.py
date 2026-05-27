import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.purchase import Purchase
from app.models.original.user_purchase import UserPurchase
from app.views.common import success

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    purchases = UserPurchase.objects.getAll(user_id, shop_id)

    if purchases:
        # 批量添加
        for purchase in purchases:
            purchase_id = purchase['purchase_id']
            order_id = purchase['order_id']
            payment = purchase['payment']
            freight = purchase['freight']
            total = purchase['total']
            order_status = purchase['order_status']
            create_time = purchase['create_time']
            product_name = purchase['product_name']
            purchase_note = purchase['purchase_note']
            find_object = Purchase.objects.getById(shop_id, purchase_id)
            if find_object:
                Purchase.objects.set(find_object['id'], order_status)
            else:
                Purchase.objects.add(shop_id, purchase_id, order_id, payment, freight, total, order_status, create_time, product_name, purchase_note)

        # 清空临时数据
        UserPurchase.objects.deleteAll(user_id, shop_id)

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    order_status = int(post.get('status'))
    Purchase.objects.set(pk, order_status)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Purchase.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    search = post.get('search')
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = Purchase.objects.total(shop_id, start_date, end_date, search)
    datas = Purchase.objects.getList(shop_id, page, num, start_date, end_date, search)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
