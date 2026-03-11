import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.transfer import Transfer
from app.models.original.user_transfer import UserTransfer

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    transfers = UserTransfer.objects.getAll(user_id, shop_id)

    # 批量合并
    for transfer in transfers:
        create_time = transfer['create_time']
        if Transfer.objects.getByCTime(shop_id, create_time):
            continue
        Transfer.objects.add(shop_id, transfer['user_name'], transfer['payee_name'], transfer['order_id'], transfer['amount'], create_time, transfer['transfer_note'])

    # 清空临时数据
    UserTransfer.objects.deleteAll(user_id, shop_id)

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
    Transfer.objects.delete(pk)
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
    total = Transfer.objects.total(shop_id)
    transfers = Transfer.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': transfers
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
