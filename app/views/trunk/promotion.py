import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.promotion import Promotion
from app.models.original.user_promotion import UserPromotion
from app.views.common import success

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid') or request.user_id)
    promotions = UserPromotion.objects.getAll(user_id, shop_id)

    if promotions:
        # 批量添加
        for promotion in promotions:
            create_date = promotion['create_date']
            promotion_type = promotion['promotion_type']
            if Promotion.objects.getByDate(shop_id, create_date, promotion_type):
                continue
            Promotion.objects.add(shop_id, create_date, promotion['payment'], promotion_type, promotion['promotion_note'])

        # 清空临时数据
        UserPromotion.objects.deleteAll(user_id, shop_id)

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    Promotion.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    start_date = datetime.strptime(post.get('sdate'), '%Y-%m-%d').date() if post.get('sdate') else None
    end_date = datetime.strptime(post.get('edate'), '%Y-%m-%d').date() if post.get('edate') else None
    total = Promotion.objects.total(shop_id, start_date, end_date)
    datas = Promotion.objects.getList(shop_id, page, num, start_date, end_date)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
