import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.deduction import Deduction

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    deductions = post.get('d')

    # 批量添加
    for deduction in deductions:
        order_id = deduction['oid']
        amount = deduction['amount']
        amount_type = int(deduction['atype'])
        create_time = deduction['ctime']
        deduction = Deduction.objects.add(shop_id, order_id, amount, amount_type, create_time)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Deduction.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Deduction.objects.total()
    deductions = Deduction.objects.getList(shop_id, page, num)
    data = Deduction.objects.encoderList(deductions)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
