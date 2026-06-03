import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt_from import ReceiptFrom
from app.models.middle.receipt_item import ReceiptItem
from app.services.receipt_ocr import ReceiptOCR
from app.views.common import failed, success

@require_POST
@transaction.atomic
def add(request):
    upload_file = request.FILES.get('file')
    if upload_file:
        shop_id = int(request.POST.get('id'))
        try:
            lines = ReceiptOCR.recognize_upload(upload_file)
            text = ReceiptOCR.get_text(lines)
            items = ReceiptItem.objects.getList(1, 1000) or []
            data = ReceiptOCR.parse_common(text, items)
            ReceiptFrom.objects.add(shop_id, data['create_date'], request.user_id, data['project_id'], data['project_num'], data['receipt_note'])
        except (RuntimeError, ValueError) as exc:
            return JsonResponse(failed(str(exc)), encoder=MyJSONEncoder)
        response = success()
        return JsonResponse(response, encoder=MyJSONEncoder)

    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    create_date = post.get('cdate')
    user_id = request.user_id
    project_id = int(post.get('name'))
    project_num = int(post.get('num'))
    receipt_note = post.get('note')
    ReceiptFrom.objects.add(shop_id, create_date, user_id, project_id, project_num, receipt_note)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    ReceiptFrom.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = ReceiptFrom.objects.total(shop_id)
    datas = ReceiptFrom.objects.getList(shop_id, page, num)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
