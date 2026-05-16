import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.trunk.deduction import Deduction
from app.models.original.user_deduction import UserDeduction
from app.models.original.user_deduction_discard import UserDeductionDiscard
from app.views.common import success

@require_POST
@transaction.atomic
def merge(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
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

    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    Deduction.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    search = post.get('search')
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = Deduction.objects.total(shop_id, start_date, end_date, search)
    datas = Deduction.objects.getList(shop_id, page, num, start_date, end_date, search)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
