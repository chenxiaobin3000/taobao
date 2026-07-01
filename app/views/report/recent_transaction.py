import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app.json_encoder import MyJSONEncoder
from app.models.const.good_follow import GoodFollowStatus
from app.models.const.order_status import OrderStatus
from app.models.middle.order_summary import OrderSummary
from app.models.system.good import Good
from app.models.system.good_follow import GoodFollow
from app.views.common import failed, success


@require_POST
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    follow = int(post.get('follow'))

    try:
        start_date = datetime.strptime(post.get('sdate'), '%Y-%m-%d')
        end_date = datetime.strptime(post.get('edate'), '%Y-%m-%d') + timedelta(days=1)
    except (TypeError, ValueError):
        return JsonResponse(failed('日期格式异常'), encoder=MyJSONEncoder)

    if start_date >= end_date:
        return JsonResponse(failed('开始日期不能晚于结束日期'), encoder=MyJSONEncoder)

    good_ids = OrderSummary.objects.getTransactionGoodIds(
        shop_id,
        start_date,
        end_date,
        Decimal('10'),
        [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.SUCCESS]
    )
    follow_ids = set(GoodFollow.objects.getGoodIds(shop_id))

    if follow == GoodFollowStatus.HAS_FOLLOW:
        good_ids &= follow_ids
    elif follow == GoodFollowStatus.NOT_FOLLOW:
        good_ids -= follow_ids
    elif follow != GoodFollowStatus.ALL:
        return JsonResponse(failed('关注类型异常'), encoder=MyJSONEncoder)

    goods = Good.objects.getListInIds(shop_id, good_ids) or []
    priority_map = GoodFollow.objects.getPriorityMap(shop_id)
    for good in goods:
        good['priority'] = priority_map.get(good['good_id'], 0)

    goods.sort(
        key=lambda good: (
            good['priority'],
            Good.objects.goodIdSortValue(good['good_id'])
        ),
        reverse=True
    )
    return JsonResponse(success({'list': goods}), encoder=MyJSONEncoder)
