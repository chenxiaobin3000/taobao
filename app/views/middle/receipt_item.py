import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt_from import ReceiptFrom
from app.models.middle.receipt_item import ReceiptItem
from app.models.middle.receipt_to import ReceiptTo
from app.views.common import failed, success

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    project_name = post.get('name')
    project_note = post.get('note')
    ReceiptItem.objects.add(project_name, project_note)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    project_name = post.get('name')
    project_note = post.get('note')
    ReceiptItem.objects.set(pk, project_name, project_note)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    if ReceiptFrom.objects.filter(project_id=pk).exists():
        return JsonResponse(failed('发票项已被进项票使用，不能删除'), encoder=MyJSONEncoder)
    if ReceiptTo.objects.filter(project_id=pk).exists():
        return JsonResponse(failed('发票项已被发票使用，不能删除'), encoder=MyJSONEncoder)
    ReceiptItem.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = ReceiptItem.objects.total()
    datas = ReceiptItem.objects.getList(page, num)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
