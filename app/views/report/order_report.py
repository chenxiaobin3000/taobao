import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.report.order import Order
from app.models.const.order_status import OrderStatus
from app.models.system.good import Good

# 刷新订单中间表
@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    status = int(post.get('status'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = []
    datas = None
    if status == OrderStatus.OTHER:
        total = Order().total(shop_id)
        datas = Order().getList(shop_id, page, num)
    else:
        total = Order().totalByStatus(shop_id, status)
        datas = Order().getListByStatus(shop_id, status, page, num)

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
                        data['good_names'] = good['short_name'] + ' | '
            if len(data['good_names']) > 3:
                data['good_names'] = data['good_names'][:-3]

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total['total'],
            'payment': total['payment'],
            'refund_customer': total['refund_customer'],
            'refund_platform': total['refund_platform'],
            'procure': total['procure'],
            'refund_procure': total['refund_procure'],
            'transfer': total['transfer'],
            'deduction': total['deduction'],
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
