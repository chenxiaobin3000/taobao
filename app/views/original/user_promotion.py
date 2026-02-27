import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_promotion import UserPromotion

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    promotions = post.get('p')

    # 批量添加
    for promotion in promotions:
        create_date = promotion['d']
        payment = promotion['p']
        promotion_type = promotion['t']
        promotion_note = promotion['n']
        if UserPromotion.objects.getByCDate(user_id, shop_id, create_date, promotion_type):
            continue
        UserPromotion.objects.add(user_id, shop_id, create_date, payment, promotion_type, promotion_note)

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
    UserPromotion.objects.delete(pk)
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
    user_id = int(post.get('uid'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = UserPromotion.objects.total(user_id, shop_id)
    promotions = UserPromotion.objects.getList(user_id, shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': promotions
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
