import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.deduction import Deduction
from app.models.original.deduction_discard import DeductionDiscard
from app.models.const.deduction_type import DeductionType

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    deductions = post.get('d')
    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }

    # 批量添加
    for deduction in deductions:
        order_id = deduction['o']
        amount = deduction['a']
        amount_type = int(deduction['t'])
        create_time = deduction['c']
        deduction_note = deduction['n']

        # 未知数据类型返回失败
        if DeductionType.OTHER == amount_type:
            response['code'] = -1
            response['msg'] = '异常数据'
            return JsonResponse(response, encoder=MyJSONEncoder)
        
        # 不处理的数据放废弃表
        if DeductionType.TUI_KUAN == amount_type or DeductionType.ZHUAN_ZHANG == amount_type:
            if DeductionDiscard.objects.getByCTime(shop_id, order_id, create_time):
                continue
            DeductionDiscard.objects.add(shop_id, order_id, amount, amount_type, create_time, deduction_note)
        else:
            if Deduction.objects.getByCTime(shop_id, order_id, create_time):
                continue
            Deduction.objects.add(shop_id, order_id, amount, amount_type, create_time, deduction_note)

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
