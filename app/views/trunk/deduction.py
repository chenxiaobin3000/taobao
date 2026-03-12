import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.deduction import Deduction
from app.models.original.user_deduction import UserDeduction
from app.models.original.user_deduction_discard import UserDeductionDiscard

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    deductions = UserDeduction.objects.getAll(user_id, shop_id)

    if deductions:
        # 批量添加
        for deduction in deductions:
            order_id = deduction['order_id']
            amount_type = int(deduction['amount_type'])
            create_time = deduction['create_time']
            if Deduction.objects.getByCTime(shop_id, order_id, amount_type, create_time):
                continue
            Deduction.objects.add(shop_id, order_id, deduction['finance_type'], deduction['amount'], amount_type, create_time, deduction['deduction_note'])

        # 清空临时数据
        UserDeduction.objects.deleteAll(user_id, shop_id)
        UserDeductionDiscard.objects.deleteAll(user_id, shop_id)

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
    Deduction.objects.delete(pk)
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
    total = Deduction.objects.total(shop_id)
    deductions = Deduction.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': deductions
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
