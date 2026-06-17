import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt_from import ReceiptFrom
from app.models.middle.receipt_item import ReceiptItem
from app.models.middle.receipt_to import ReceiptTo
from app.views.common import success


def build_project_map():
    items = ReceiptItem.objects.getList(1, 10000) or []
    return {item['id']: item['project_name'] for item in items}


def add_project_num(result, receipt, key):
    if receipt.project_id not in result:
        result[receipt.project_id] = {
            'project_id': receipt.project_id,
            'from_num': 0,
            'to_num': 0
        }
    result[receipt.project_id][key] += receipt.project_num


def build_invoice_list(from_receipts, to_receipts, project_map):
    result = {}
    for receipt in from_receipts:
        add_project_num(result, receipt, 'from_num')
    for receipt in to_receipts:
        add_project_num(result, receipt, 'to_num')

    datas = []
    for project_id, item in result.items():
        from_num = item['from_num']
        to_num = item['to_num']
        has_from = from_num > 0
        has_to = to_num > 0
        check_text = ''
        check_success = True
        if has_to and has_from:
            if from_num >= to_num:
                check_text = '已开'
            else:
                check_text = f'缺少{to_num - from_num}'
                check_success = False
        elif has_to:
            check_text = f'缺少{to_num}'
            check_success = False

        if has_to and has_from:
            sort_type = 0
        elif has_to:
            sort_type = 1
        else:
            sort_type = 2

        project_name = project_map.get(project_id, '异常')
        datas.append({
            'project_id': project_id,
            'to_text': project_name if has_to else '',
            'to_num': to_num if has_to else '',
            'from_text': project_name if has_from else '',
            'from_num': from_num if has_from else '',
            'check_text': check_text,
            'check_success': check_success,
            'receipt_note': '',
            'has_to': has_to,
            '_sort_type': sort_type
        })

    datas = sorted(datas, key=lambda item: (item['_sort_type'], item['project_id']))
    for item in datas:
        item.pop('_sort_type')
    return datas


@require_POST
def getList(request):
    post = json.loads(request.body)
    end_date = post.get('edate')
    start_date = post.get('sdate')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=183)).strftime('%Y-%m-%d')

    project_map = build_project_map()
    from_receipts = ReceiptFrom.objects.filter(create_date__gte=start_date, create_date__lte=end_date).order_by('create_date', 'id')
    to_receipts = ReceiptTo.objects.filter(create_date__gte=start_date, create_date__lte=end_date).order_by('create_date', 'id')
    datas = build_invoice_list(from_receipts, to_receipts, project_map)
    response = success({
            'total': len(datas),
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
