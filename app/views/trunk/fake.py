import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.good_type import GoodType
from app.models.trunk.fake import Fake
from app.models.system.good import Good

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
