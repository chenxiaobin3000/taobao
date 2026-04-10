import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.receipt import Receipt

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    create_date = post.get('cdate')
    user_id = int(post.get('uid'))
    project_name = post.get('name')
    amount = post.get('amount')
    misc_note = post.get('note')
    Receipt.objects.add(shop_id, create_date, user_id, project_name, amount, misc_note)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    create_date = post.get('cdate')
    user_id = int(post.get('uid'))
    project_name = post.get('name')
    amount = post.get('amount')
    misc_note = post.get('note')
    Receipt.objects.set(pk, create_date, user_id, project_name, amount, misc_note)
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
    Receipt.objects.delete(pk)
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
    total = Receipt.objects.total(shop_id)
    datas = Receipt.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
