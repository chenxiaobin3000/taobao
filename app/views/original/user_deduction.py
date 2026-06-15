import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.deduction_type import DeductionType
from app.models.original.user_deduction import UserDeduction
from app.models.original.user_deduction_discard import UserDeductionDiscard
from app.views.common import failed, success

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    deductions = post.get('d')
    response = success()

    # 批量添加
    for deduction in deductions:
        order_id = deduction['o']
        finance_type = deduction['f']
        amount = deduction['a']
        amount_type = int(deduction['t'])
        create_time = deduction['c']
        deduction_note = deduction['n']

        # 未知数据类型返回失败
        if DeductionType.OTHER == amount_type:
            return JsonResponse(failed('异常数据'), encoder=MyJSONEncoder)

        # 不处理的数据放废弃表
        if DeductionType.TUI_KUAN == amount_type or DeductionType.ZHUAN_ZHANG == amount_type or DeductionType.BAO_ZHENG_JIN == amount_type or DeductionType.DA_KUAN == amount_type or DeductionType.CHONG_ZHI == amount_type or DeductionType.ONLINE == amount_type or DeductionType.OTHER == amount_type:
            if UserDeductionDiscard.objects.getByCTime(user_id, shop_id, order_id, amount_type, create_time):
                continue
            UserDeductionDiscard.objects.add(user_id, shop_id, order_id, finance_type, amount, amount_type, create_time, deduction_note)
        else:
            if UserDeduction.objects.getByCTime(user_id, shop_id, order_id, amount_type, create_time):
                continue
            UserDeduction.objects.add(user_id, shop_id, order_id, finance_type, amount, amount_type, create_time, deduction_note)

    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserDeduction.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = request.user_id
    UserDeduction.objects.deleteAll(user_id, id)
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
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = UserDeduction.objects.total(user_id, shop_id, start_date, end_date, search)
    deductions = UserDeduction.objects.getList(user_id, shop_id, page, num, start_date, end_date, search)
    response = success({
            'total': total,
            'list': deductions
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
