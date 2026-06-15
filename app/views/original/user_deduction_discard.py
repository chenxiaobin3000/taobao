import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_deduction_discard import UserDeductionDiscard
from app.views.common import success

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserDeductionDiscard.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = request.user_id
    UserDeductionDiscard.objects.deleteAll(user_id, id)
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
    total = UserDeductionDiscard.objects.total(user_id, shop_id, start_date, end_date, search)
    deductions = UserDeductionDiscard.objects.getList(user_id, shop_id, page, num, start_date, end_date, search)
    response = success({
            'total': total,
            'list': deductions
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
