import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt_from import ReceiptFrom
from app.models.middle.receipt_item import ReceiptItem
from app.models.middle.receipt_owner import ReceiptOwner
from app.services.receipt_ocr import ReceiptOCR
from app.views.common import failed, success

def validate_receipt_owner(company, company_id):
    if ReceiptOwner.objects.total() <= 0:
        raise ValueError('请先在公司信息中登记公司发票信息')
    if not ReceiptOwner.objects.existsOwner(company, company_id):
        raise ValueError(f'购买方不在公司发票登记中：{company} {company_id}')

def create_receipt_item(project_name):
    item = ReceiptItem.objects.add(project_name, 'OCR自动添加')
    return {
        'id': item.id,
        'project_name': item.project_name,
        'project_note': item.project_note
    }

@require_POST
@transaction.atomic
def add(request):
    upload_file = request.FILES.get('file')
    if upload_file:
        shop_id = int(request.POST.get('id'))
        text = ''
        try:
            lines = ReceiptOCR.recognize_upload(upload_file)
            text = ReceiptOCR.get_text(lines)
            items = ReceiptItem.objects.getList(1, 1000) or []
            data = ReceiptOCR.parse_common(text, items, create_receipt_item)
            print('[receipt_from_ocr]', upload_file.name, text, json.dumps(data, ensure_ascii=False, default=str), flush=True)
            validate_receipt_owner(ReceiptOCR._parse_receipt_name(text), ReceiptOCR._parse_company_id(text))
            if ReceiptFrom.objects.existsReceipt(data['receipt_id']):
                return JsonResponse(success({'duplicate': True}), encoder=MyJSONEncoder)
            ReceiptFrom.objects.add(shop_id, data['create_date'], request.user_id, data['project_id'], data['project_num'], data['receipt_id'], data['receipt_note'], data['amount'], data['tax'], data['tax_rate'], data['company'], data['company_id'])
        except (RuntimeError, ValueError) as exc:
            print('[receipt_from_ocr_error]', upload_file.name, str(exc), text, flush=True)
            return JsonResponse(failed(str(exc)), encoder=MyJSONEncoder)
        response = success()
        return JsonResponse(response, encoder=MyJSONEncoder)

    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    create_date = post.get('cdate')
    user_id = request.user_id
    project_id = int(post.get('name'))
    project_num = int(post.get('num'))
    receipt_id = post.get('receipt_id')
    amount = post.get('amount')
    tax = post.get('tax')
    tax_rate = int(post.get('tax_rate'))
    company = post.get('company')
    company_id = post.get('company_id', '')
    receipt_note = post.get('note')
    if ReceiptFrom.objects.existsReceipt(receipt_id):
        return JsonResponse(success({'duplicate': True}), encoder=MyJSONEncoder)
    ReceiptFrom.objects.add(shop_id, create_date, user_id, project_id, project_num, receipt_id, receipt_note, amount, tax, tax_rate, company, company_id)
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
