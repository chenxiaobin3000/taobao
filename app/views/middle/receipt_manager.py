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


def append_receipts(result, receipts, project_map, key):
    for receipt in receipts:
        row = get_row(result, receipt.create_date)
        project_name = project_map.get(receipt.project_id, '异常')
        text = f'{project_name}*{receipt.project_num}'
        if row[key]:
            row[key] += f';{text}'
        else:
            row[key] = text
        if key == 'to_text':
            row['has_to'] = True


def get_row(result, create_date):
    date_key = create_date.strftime('%Y-%m-%d')
    if date_key not in result:
        result[date_key] = {
            'create_date': date_key,
            'from_text': '',
            'to_text': '',
            'check_text': '',
            'check_success': True,
            '_missing': {},
            'has_to': False
        }
    return result[date_key]


def append_text(row, key, text):
    if row[key]:
        row[key] += f';{text}'
    else:
        row[key] = text


def build_events(from_receipts, to_receipts):
    events = []
    for receipt in from_receipts:
        events.append((receipt.create_date, 0, receipt.id, receipt))
    for receipt in to_receipts:
        events.append((receipt.create_date, 1, receipt.id, receipt))
    return sorted(events, key=lambda item: (item[0], item[1], item[2]))


def format_missing(missing, project_map):
    return ';'.join([f"{project_map.get(project_id, '异常')}*{num}" for project_id, num in missing.items() if num > 0])


def finalize_rows(result, project_map):
    for row in result.values():
        missing_text = format_missing(row['_missing'], project_map)
        if missing_text:
            row['check_text'] = missing_text
            row['check_success'] = False
        elif row['has_to']:
            row['check_text'] = '已开'
            row['check_success'] = True
        row.pop('_missing')


def build_invoice_list(from_receipts, to_receipts, project_map):
    result = {}
    available = {}
    missing = {}
    for create_date, receipt_type, pk, receipt in build_events(from_receipts, to_receipts):
        row = get_row(result, create_date)
        project_name = project_map.get(receipt.project_id, '异常')
        text = f'{project_name}*{receipt.project_num}'
        if receipt_type == 0:
            append_text(row, 'from_text', text)
            available[receipt.project_id] = available.get(receipt.project_id, 0) + receipt.project_num
            continue

        append_text(row, 'to_text', text)
        row['has_to'] = True
        current = available.get(receipt.project_id, 0)
        if current >= receipt.project_num:
            available[receipt.project_id] = current - receipt.project_num
        else:
            available[receipt.project_id] = 0
            missing_num = receipt.project_num - current
            missing[receipt.project_id] = missing.get(receipt.project_id, 0) + missing_num
            row['_missing'][receipt.project_id] = row['_missing'].get(receipt.project_id, 0) + missing_num
    finalize_rows(result, project_map)
    datas = sorted(result.values(), key=lambda item: item['create_date'], reverse=True)
    missing_text = format_missing(missing, project_map)
    return datas, missing_text


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
    datas, missing_text = build_invoice_list(from_receipts, to_receipts, project_map)
    response = success({
            'total': len(datas),
            'list': datas,
            'missing': missing_text
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
