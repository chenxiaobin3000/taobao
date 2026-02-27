import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.polymerize import Polymerize
from app.models.const.deduction_type import DeductionType

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    polymerizes = post.get('p')
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 批量添加
    for polymerize in polymerizes:
        order_id = polymerize['o']
        amount = polymerize['a']
        amount_type = int(polymerize['t'])
        create_time = polymerize['c']
        polymerize_note = polymerize['n']

        # 未知数据类型返回失败
        if DeductionType.OTHER == amount_type:
            response['code'] = -1
            response['msg'] = '异常数据'
            return JsonResponse(response, encoder=MyJSONEncoder)
        
        # 插入数据
        if Polymerize.objects.getByCTime(shop_id, order_id, amount_type, create_time):
            continue
        Polymerize.objects.add(shop_id, order_id, amount, amount_type, create_time, polymerize_note)

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    Polymerize.objects.delete(pk)
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
    total = Polymerize.objects.total(shop_id)
    polymerizes = Polymerize.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': polymerizes
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
