import json
from decimal import Decimal
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_purchase import UserPurchase
from app.views.common import success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    user_id = request.user_id
    purchases = post.get('p')

    # 批量添加
    for purchase in purchases:
        purchase_id = purchase['pid']
        purchase_account = purchase.get('pa') or ''
        payment = purchase['payment']
        freight = purchase['freight']
        total = purchase['total']
        order_status = purchase['status']
        create_time = purchase['ctime']
        product_name = purchase['pn']
        purchase_note = ''
        find_object = UserPurchase.objects.getByPurchaseId(user_id, purchase_id)
        if find_object:
            payment = Decimal(str(payment))
            freight = Decimal(str(freight))
            total = Decimal(str(total))
            order_status = int(order_status)
            if find_object.purchase_account == purchase_account and find_object.payment == payment and find_object.freight == freight and find_object.total == total and find_object.order_status == order_status:
                continue
            find_object.purchase_account = purchase_account
            find_object.payment = payment
            find_object.freight = freight
            find_object.total = total
            find_object.order_status = order_status
            find_object.save(update_fields=['purchase_account', 'payment', 'freight', 'total', 'order_status'])
        else:
            UserPurchase.objects.add(user_id, purchase_id, purchase_account, payment, freight, total, order_status, create_time, product_name, purchase_note)

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    order_status = int(post.get('status'))
    UserPurchase.objects.set(pk, order_status)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserPurchase.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    user_id = request.user_id
    UserPurchase.objects.deleteAll(user_id)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
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
    total = UserPurchase.objects.total(user_id, start_date, end_date, search)
    purchases = UserPurchase.objects.getList(user_id, page, num, start_date, end_date, search)
    response = success({
            'total': total,
            'list': purchases
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
