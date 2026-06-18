import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt_from import ReceiptFrom
from app.models.middle.receipt_item import ReceiptItem
from app.models.middle.receipt_map import ReceiptMap
from app.models.middle.receipt_to import ReceiptTo
from app.models.system.shop import Shop
from app.views.common import failed, success


def build_project_map():
    items = ReceiptItem.objects.getList(1, 10000) or []
    return {item['id']: item['project_name'] for item in items}


def add_project_num(result, project_id, project_num, key):
    if project_id not in result:
        result[project_id] = {
            'project_id': project_id,
            'from_num': 0,
            'to_num': 0
        }
    result[project_id][key] += project_num


def build_invoice_list(from_receipts, to_receipts, project_map):
    result = {}
    project_shop_ids = {}
    mapped_item_ids = {}
    receipt_map = ReceiptMap.objects.getMap()
    for receipt in from_receipts:
        source_project_id = receipt.project_id
        target_project_id = receipt_map.get(source_project_id, source_project_id)
        add_project_num(result, target_project_id, receipt.project_num, 'from_num')
        project_shop_ids.setdefault(target_project_id, set()).add(receipt.shop_id)
        if target_project_id != source_project_id:
            mapped_item_ids.setdefault(target_project_id, set()).add(source_project_id)
    for receipt in to_receipts:
        add_project_num(result, receipt.project_id, receipt.project_num, 'to_num')

    shop_ids = set()
    for values in project_shop_ids.values():
        shop_ids.update(values)
    shop_map = dict(Shop.objects.filter(id__in=shop_ids).values_list('id', 'name'))

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
        elif has_from:
            sort_type = 1
        else:
            sort_type = 2

        project_name = project_map.get(project_id, '异常')
        source_names = [
            project_map.get(source_id, '异常')
            for source_id in sorted(mapped_item_ids.get(project_id, set()))
        ]
        shop_names = [
            shop_map[shop_id]
            for shop_id in sorted(project_shop_ids.get(project_id, set()))
            if shop_id in shop_map
        ]
        to_text = project_name
        from_text = project_name
        if source_names:
            from_text += f"[{'、'.join(source_names)}]"
        if shop_names:
            from_text += f"（{'、'.join(shop_names)}）"
        datas.append({
            'project_id': project_id,
            'to_text': to_text if has_to else '',
            'to_num': to_num if has_to else '',
            'from_text': from_text if has_from else '',
            'from_num': from_num if has_from else '',
            'check_text': check_text,
            'check_success': check_success,
            'receipt_note': '已关联' if source_names else '',
            'has_to': has_to,
            'has_from': has_from,
            '_sort_type': sort_type,
            '_sort_name': project_name
        })

    datas = sorted(datas, key=lambda item: (item['_sort_type'], item['_sort_name']))
    for item in datas:
        item.pop('_sort_type')
        item.pop('_sort_name')
    return datas


@require_POST
def setMap(request):
    post = json.loads(request.body)
    item_id = int(post.get('item_id'))
    map_id = int(post.get('map_id'))
    if item_id == map_id:
        return JsonResponse(failed('进项项目不能关联自身'), encoder=MyJSONEncoder)
    item_ids = set(ReceiptItem.objects.filter(id__in=[item_id, map_id]).values_list('id', flat=True))
    if item_ids != {item_id, map_id}:
        return JsonResponse(failed('发票项目不存在'), encoder=MyJSONEncoder)
    if not ReceiptFrom.objects.filter(project_id=item_id).exists():
        return JsonResponse(failed('关联项目不存在进项数据'), encoder=MyJSONEncoder)
    if not ReceiptTo.objects.filter(project_id=map_id).exists():
        return JsonResponse(failed('目标项目不存在出项数据'), encoder=MyJSONEncoder)
    ReceiptMap.objects.set(item_id, map_id)
    return JsonResponse(success(), encoder=MyJSONEncoder)


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
