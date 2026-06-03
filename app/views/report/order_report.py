import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.order_status import OrderStatus
from app.models.report.native_order import NativeOrder
from app.models.system.good import Good
from app.views.common import success

# 刷新订单中间表
@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    status = int(post.get('status'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    search = post.get('search')
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    good_id_search = None
    if search:
        keyword = str(search).strip()
        good = Good.objects.getById(shop_id, keyword)
        if good:
            good_id_search = good['good_id']
            search = None
    total = []
    datas = None
    if status == OrderStatus.OTHER:
        total = NativeOrder().total(shop_id, start_date, end_date, search, good_id_search)
        datas = NativeOrder().getList(shop_id, page, num, start_date, end_date, search, good_id_search)
    else:
        total = NativeOrder().totalByStatus(shop_id, status, start_date, end_date, search, good_id_search)
        datas = NativeOrder().getListByStatus(shop_id, status, page, num, start_date, end_date, search, good_id_search)

    # 解析商品名称
    if datas:
        for data in datas:
            goods = data['good_ids']
            if not goods:
                continue
            gids = goods.split('|')
            data['good_names'] = ''
            for gid in gids:
                if gid:
                    good = Good.objects.getById(shop_id, gid)
                    if good:
                        data['good_names'] = data['good_names'] + good['short_name'] + ' | '
            if len(data['good_names']) > 3:
                data['good_names'] = data['good_names'][:-3]

    response = success({
            'total': round(total['total'], 2),
            'payment': round(total['payment'], 2),
            'refund_customer': round(total['refund_customer'], 2),
            'refund_platform': round(total['refund_platform'], 2),
            'procure': round(total['procure'], 2),
            'refund_procure': round(total['refund_procure'], 2),
            'transfer': round(total['transfer'], 2),
            'deduction': round(total['deduction'], 2),
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
