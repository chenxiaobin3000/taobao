import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt_owner import ReceiptOwner
from app.views.common import success


@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    company = post.get('company')
    company_id = post.get('company_id')
    ReceiptOwner.objects.add(company, company_id)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    ReceiptOwner.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = ReceiptOwner.objects.total()
    datas = ReceiptOwner.objects.getList(page, num)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
