import json
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
    user_id = request.user_id
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
    total = Promotion.objects.total(shop_id)
    datas = Promotion.objects.getList(shop_id, page, num)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
