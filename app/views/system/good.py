import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.middle.order_summary import OrderSummary
from app.models.system.good import Good
from app.models.system.good_alias import GoodAlias
from app.models.system.good_follow import GoodFollow
from app.services.good_init_zip import build_init_zip
from app.models.trunk.fake import Fake
from app.models.trunk.promotion_detail import PromotionDetail
from app.views.common import failed, success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    goods = post.get('g')
    response = success()

    # 批量添加
    for good in goods:
        find_object = Good.objects.getById(shop_id, good['i'])
        if find_object:
            Good.objects.set(find_object['id'], good['n'], good['sn'], good['t'], good['s'], good['o'], good['ot'], good['st'], good['stt'])
        else:
            Good.objects.add(shop_id, good['i'], good['n'], good['sn'], good['t'], good['s'], good['o'], good['ot'], good['st'], good['stt'])

        # 处理优先级
        priority = int(good.get('p'))
        follow = GoodFollow.objects.getByGood(shop_id, good['i'])
        if priority > 0:
            if follow:
                GoodFollow.objects.set(follow['id'], priority)
            else:
                GoodFollow.objects.add(shop_id, good['i'], priority)
        elif follow:
            GoodFollow.objects.delete(follow['id'])

        # 处理别名
        for alias in good['as']:
            if alias:
                find_object = GoodAlias.objects.getByName(shop_id, alias)
                if not find_object:
                    GoodAlias.objects.add(shop_id, good['i'], alias)

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    goods = Good.objects.getList(shop_id, 1, 1000)
    if goods:
        for good in goods:
            # 首次刷单时间
            if not good['fake_date']:
                fake = Fake.objects.getByGood(shop_id, good['good_id'] + '|')
                if fake:
                    Good.objects.setFakeDate(good['id'], fake['create_time'])

            # 首次推广时间
            if not good['promotion_date']:
                promotion = PromotionDetail.objects.getByGood(shop_id, good['good_id'])
                if promotion:
                    Good.objects.setPromotionDate(good['id'], promotion['promotion_date'])

    order_start_date = timezone.now() - timedelta(days=30)
    promotion_start_date = datetime.now().date() - timedelta(days=30)
    order_good_ids = OrderSummary.objects.getGoodIdsByDate(shop_id, order_start_date, 10)
    promotion_good_ids = PromotionDetail.objects.getGoodIdsByDate(shop_id, promotion_start_date)
    GoodFollow.objects.refreshPriority(shop_id, order_good_ids, promotion_good_ids)

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    name = post.get('name')
    short_name = post.get('sname')
    good_type = int(post.get('type'))
    good_status = int(post.get('status'))
    origin = post.get('origin')
    origin_type = int(post.get('origin_type'))
    stock = post.get('stock')
    stock_type = int(post.get('stock_type'))
    Good.objects.set(pk, name, short_name, good_type, good_status, origin, origin_type, stock, stock_type)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    Good.objects.delete(pk)
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
    good_type = int(post.get('type'))
    good_status = int(post.get('status'))
    follow = int(post.get('follow'))
    follow_ids = GoodFollow.objects.getGoodIds(shop_id)
    follow_priority_map = GoodFollow.objects.getPriorityMap(shop_id)
    total = Good.objects.total(shop_id, search, good_type, good_status, follow, follow_ids)
    datas = Good.objects.getList(shop_id, page, num, search, good_type, good_status, follow, follow_ids, follow_priority_map)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getInitZip(request):
    post = json.loads(request.body)
    company_id = int(post.get('id'))
    user_id = request.user_id
    try:
        data = build_init_zip(company_id, user_id)
    except ValueError as exc:
        return JsonResponse(failed(str(exc)), encoder=MyJSONEncoder)

    response = HttpResponse(data, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="data_import_init.zip"'
    return response
