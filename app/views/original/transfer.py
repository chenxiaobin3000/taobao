import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.original.transfer import Transfer

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    transfers = post.get('t')

    # 批量添加
    for transfer in transfers:
        user_id = int(transfer['uid'])
        order_id = transfer['oid']
        amount = transfer['amount']
        create_time = transfer['ctime']
        Transfer.objects.add(shop_id, user_id, order_id, amount, create_time)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Transfer.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    transfers = Transfer.objects.getList(shop_id, page, num)
    data = Transfer.objects.encoderList(transfers)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
