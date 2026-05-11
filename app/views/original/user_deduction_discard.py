import json
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
    user_id = request.user_id
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = UserDeductionDiscard.objects.total(user_id, shop_id)
    deductions = UserDeductionDiscard.objects.getList(user_id, shop_id, page, num)
    response = success({
            'total': total,
            'list': deductions
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
