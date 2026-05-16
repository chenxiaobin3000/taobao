import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_transfer import UserTransfer
from app.views.common import success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    transfers = post.get('t')

    # 批量添加
    for transfer in transfers:
        user_name = transfer['n']
        payee_name = transfer['p']
        order_id = transfer['o']
        amount = transfer['a']
        create_time = transfer['c']
        transfer_note= transfer['tn'] if 'tn' in transfer else ''
        if UserTransfer.objects.getByCTime(user_id, shop_id, create_time):
            continue
        UserTransfer.objects.add(user_id, shop_id, user_name, payee_name, order_id, amount, create_time, transfer_note)

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserTransfer.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = request.user_id
    UserTransfer.objects.deleteAll(user_id, id)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    page = int(post.get('page'))
    num = int(post.get('num'))
    search = post.get('search')
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = UserTransfer.objects.total(user_id, shop_id, start_date, end_date, search)
    transfers = UserTransfer.objects.getList(user_id, shop_id, page, num, start_date, end_date, search)
    response = success({
            'total': total,
            'list': transfers
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
