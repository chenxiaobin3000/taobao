import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.deduction_type import DeductionType
from app.models.original.user_polymerize import UserPolymerize
from app.models.original.user_polymerize_discard import UserPolymerizeDiscard
from app.views.common import failed, success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    polymerizes = post.get('p')
    response = success()

    # 批量添加
    for polymerize in polymerizes:
        order_id = polymerize['o']
        finance_type = polymerize['f']
        amount = polymerize['a']
        amount_type = int(polymerize['t'])
        create_time = polymerize['c']
        polymerize_note = polymerize['n']

        # 未知数据类型返回失败
        if DeductionType.OTHER == amount_type:
            return JsonResponse(failed('异常数据'), encoder=MyJSONEncoder)
        
        # 不处理的数据放废弃表
        if DeductionType.TUI_KUAN == amount_type or DeductionType.ZHUAN_ZHANG == amount_type:
            if UserPolymerizeDiscard.objects.getByCTime(user_id, shop_id, order_id, amount_type, create_time):
                continue
            UserPolymerizeDiscard.objects.add(user_id, shop_id, order_id, finance_type, amount, amount_type, create_time, polymerize_note)
        else:
            if UserPolymerize.objects.getByCTime(user_id, shop_id, order_id, amount_type, create_time):
                continue
            UserPolymerize.objects.add(user_id, shop_id, order_id, finance_type, amount, amount_type, create_time, polymerize_note)

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserPolymerize.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = request.user_id
    UserPolymerize.objects.deleteAll(user_id, id)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = int(post.get('uid') or request.user_id)
    page = int(post.get('page'))
    num = int(post.get('num'))
    search = post.get('search')
    amount_type = post.get('amount_type')
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if amount_type:
        amount_type = int(amount_type)
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = UserPolymerize.objects.total(user_id, shop_id, start_date, end_date, search, amount_type)
    polymerizes = UserPolymerize.objects.getList(user_id, shop_id, page, num, start_date, end_date, search, amount_type)
    amount_types = UserPolymerize.objects.getAmountTypes(user_id, shop_id, start_date, end_date, search)
    response = success({
            'total': total,
            'list': polymerizes,
            'amount_types': amount_types
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
