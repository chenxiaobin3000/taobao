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
        create_date = receipt.create_date.strftime('%Y-%m-%d')
        if create_date not in result:
            result[create_date] = {
                'create_date': create_date,
                'from_text': '',
                'to_text': '',
                'has_to': False
            }
        project_name = project_map.get(receipt.project_id, '异常')
        text = f'{project_name}*{receipt.project_num}'
        if result[create_date][key]:
            result[create_date][key] += f';{text}'
        else:
            result[create_date][key] = text
        if key == 'to_text':
            result[create_date]['has_to'] = True


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
    result = {}
    from_receipts = ReceiptFrom.objects.filter(create_date__gte=start_date, create_date__lte=end_date).order_by('-create_date')
    to_receipts = ReceiptTo.objects.filter(create_date__gte=start_date, create_date__lte=end_date).order_by('-create_date')
    append_receipts(result, from_receipts, project_map, 'from_text')
    append_receipts(result, to_receipts, project_map, 'to_text')
    datas = sorted(result.values(), key=lambda item: item['create_date'], reverse=True)
    response = success({
            'total': len(datas),
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
