import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.good_follow import GoodFollowStatus
from app.models.system.good import Good
from app.models.trunk.order import Order
from app.models.report.good_follow import GoodFollow
from app.models.report.native_promotion_detail import NativePromotionDetail

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    follow = int(post.get('follow'))
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    end_date = datetime.strptime(post.get('edate'), "%Y-%m-%d")
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 生成商品列表
    good = []
    match follow:
        case GoodFollowStatus.ALL:
            good = Good.objects.getList(shop_id, 1, 1000)

        case GoodFollowStatus.HAS_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if temps:
                ids = [temp['good_id'] for temp in temps]
                good = Good.objects.getListInIds(shop_id, ids)

        case GoodFollowStatus.NOT_FOLLOW:
            temps = GoodFollow.objects.getList(shop_id, 1, 1000)
            if temps:
                ids = [temp['good_id'] for temp in temps]
                good = Good.objects.getListNotInIds(shop_id, ids)

        case _:
            response['code'] = -1
            response['msg'] = '关注类型异常'
            return JsonResponse(response, encoder=MyJSONEncoder)

    # 获取订单数据
    orders= Order.objects.getListByDateRange(shop_id, start_date, end_date)
    if orders:
        # 未发货
        # 已发货
        # 交易成功
        # 交易关闭
        pass

    # 获取推广数据
    promotions= NativePromotionDetail().getListByDateRange(shop_id, start_date, end_date)
    if promotions:
        pass

    # 按利润排序

    datas = []
    response['data'] = {
        'list': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
