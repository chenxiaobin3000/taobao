import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.good_prepare import GoodPrepare
from app.models.system.good import Good

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    name = post.get('name')
    origin = post.get('origin')
    origin_type = int(post.get('origin_type'))
    good_note = post.get('note')
    GoodPrepare.objects.add(shop_id, name, origin, origin_type, good_note)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    goods = GoodPrepare.objects.getList(shop_id, 1, 1000)
    if goods:
        for good in goods:
            # 首次创建时间
            if not good['join_date']:
                temp = Good.objects.getByOrigin(shop_id, good['origin'])
                if temp:
                    Good.objects.setJoinDate(good['id'], temp['ctime'])
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
    GoodPrepare.objects.delete(pk)
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
    total = GoodPrepare.objects.total(shop_id)
    datas = GoodPrepare.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
