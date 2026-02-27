import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_transfer import UserTransfer

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    transfers = post.get('t')

    # 批量添加
    for transfer in transfers:
        user_name = transfer['n']
        payee_name = transfer['p']
        order_id = transfer['o']
        amount = transfer['a']
        create_time = transfer['c']
        transfer_note= transfer['tn']
        if UserTransfer.objects.getByCTime(shop_id, create_time):
            continue
        UserTransfer.objects.add(shop_id, user_name, payee_name, order_id, amount, create_time, transfer_note)

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
    UserTransfer.objects.delete(pk)
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
    total = UserTransfer.objects.total(shop_id)
    transfers = UserTransfer.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': transfers
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
