import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.miscellaneous import Miscellaneous
from app.views.common import success

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
    Miscellaneous.objects.add(shop_id, create_date, user_id, project_name, amount, misc_note)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    datas = post.get('m')
    miscs = []
    for data in datas:
        create_date = data.get('cdate')
        project_name = data.get('name')
        amount = data.get('amount')
        if Miscellaneous.objects.exists(shop_id, create_date, project_name, amount):
            continue
        miscs.append(Miscellaneous(
            shop_id=shop_id,
            create_date=create_date,
            user_id=int(data.get('uid')),
            project_name=project_name,
            amount=amount,
            misc_note=data.get('note')
        ))
    if len(miscs) > 0:
        Miscellaneous.objects.addList(miscs)
    response = success()
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
    Miscellaneous.objects.set(pk, create_date, user_id, project_name, amount, misc_note)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    Miscellaneous.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Miscellaneous.objects.total(shop_id)
    datas = Miscellaneous.objects.getList(shop_id, page, num)
    response = success({
            'total': total,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
