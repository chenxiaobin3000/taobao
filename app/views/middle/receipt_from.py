import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt_from import ReceiptFrom

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    create_date = post.get('cdate')
    user_id = int(post.get('uid'))
    project_id = int(post.get('name'))
    project_num = int(post.get('num'))
    receipt_note = post.get('note')
    ReceiptFrom.objects.add(create_date, user_id, project_id, project_num, receipt_note)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    ReceiptFrom.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success'
    }
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
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
