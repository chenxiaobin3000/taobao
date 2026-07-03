import json
from datetime import datetime
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_promotion import UserPromotion
from app.views.common import failed, success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    promotions = post.get('p')

    # 批量添加
    for promotion in promotions:
        create_date = promotion['d']
        payment = promotion['p']
        promotion_type = int(promotion['t'])
        promotion_note = promotion['n']
        find_object = UserPromotion.objects.getByDate(user_id, shop_id, create_date, promotion_type)
        if find_object:
            payment_decimal = Decimal(str(payment))
            if find_object['payment'] == payment_decimal and find_object['promotion_type'] == promotion_type:
                continue
            response = failed('重复数据：日期(' + create_date + ')')
            return JsonResponse(response, encoder=MyJSONEncoder)
        UserPromotion.objects.add(user_id, shop_id, create_date, payment, promotion_type, promotion_note)

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserPromotion.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = request.user_id
    UserPromotion.objects.deleteAll(user_id, id)
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
    start_date = datetime.strptime(post.get('sdate'), '%Y-%m-%d').date() if post.get('sdate') else None
    end_date = datetime.strptime(post.get('edate'), '%Y-%m-%d').date() if post.get('edate') else None
    total = UserPromotion.objects.total(user_id, shop_id, start_date, end_date)
    promotions = UserPromotion.objects.getList(user_id, shop_id, page, num, start_date, end_date)
    response = success({
            'total': total,
            'list': promotions
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
