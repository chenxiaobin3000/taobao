import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.company import Company
from app.models.system.user import User

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    name = post.get('name')
    user_id = int(post.get('uid'))
    company = Company.objects.add(name, user_id)
    data = Company.objects.encoder(company)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    name = post.get('name')
    user_id = int(post.get('uid'))
    data = Company.objects.set(pk, name, user_id)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Company.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def get(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    company = Company.objects.find(pk)
    data = Company.objects.encoder(company)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    page = int(post.get('page'))
    num = int(post.get('num'))
    companys = Company.objects.getList(page, num)
    data = Company.objects.encoderList(companys)

    # 获取负责人信息
    for company in data:
        user = User.objects.find(company['user_id'])
        company['user'] = user.name

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
