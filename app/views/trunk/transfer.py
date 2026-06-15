import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.transfer import Transfer
from app.models.original.user_transfer import UserTransfer
from app.views.common import success

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid') or request.user_id)
    transfers = UserTransfer.objects.getAll(user_id, shop_id)

    if transfers:
        # 批量合并
        for transfer in transfers:
            create_time = transfer['create_time']
            if Transfer.objects.getByCTime(shop_id, create_time):
                continue
            Transfer.objects.add(shop_id, transfer['user_name'], transfer['payee_name'], transfer['order_id'], transfer['amount'], create_time, transfer['transfer_note'])

        # 清空临时数据
        UserTransfer.objects.deleteAll(user_id, shop_id)

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    Transfer.objects.delete(pk)
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
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = Transfer.objects.total(shop_id, start_date, end_date, search)
    datas = Transfer.objects.getList(shop_id, page, num, start_date, end_date, search)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
