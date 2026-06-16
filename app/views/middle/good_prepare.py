import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.good_prepare import GoodPrepare
from app.models.system.good import Good
from app.views.common import success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    goods = post.get('g') or []
    origins = [
        str(good.get('origin')).strip()
        for good in goods
        if good.get('origin') is not None and str(good.get('origin')).strip()
    ]
    exists_origins = GoodPrepare.objects.getOrigins(shop_id, origins)
    handled_origins = set()
    for good in goods:
        origin = str(good.get('origin')).strip() if good.get('origin') is not None else ''
        if origin and (origin in exists_origins or origin in handled_origins):
            continue
        GoodPrepare.objects.add(
            shop_id,
            good.get('name'),
            origin,
            int(good.get('origin_type')),
            good.get('stock'),
            int(good.get('stock_type')),
            good.get('note') or ''
        )
        if origin:
            handled_origins.add(origin)
    response = success()
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
            if good['join_date'] is None:
                temp = Good.objects.getByOrigin(shop_id, good['origin'])
                if temp:
                    GoodPrepare.objects.setJoinDate(good['id'], temp['ctime'])
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    GoodPrepare.objects.delete(pk)
    response = success()
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
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
