import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.user import User

@require_POST
def add(request):
    post = json.loads(request.body)
    name = post.get('name')
    phone = post.get('phone')
    company_id = post.get('cid')
    role_id = post.get('rid')
    user = User.objects.add(name, phone, company_id, role_id)
    data = User.objects.encoder(user)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def set(request):
    post = json.loads(request.body)
    pk = post.get('id')
    name = post.get('name')
    phone = post.get('phone')
    company_id = post.get('cid')
    role_id = post.get('rid')
    data = User.objects.set(pk, name, phone, company_id, role_id)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def delete(request):
    post = json.loads(request.body)
    pk = post.get('id')
    data = User.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def get(request):
    post = json.loads(request.body)
    pk = post.get('id')
    good = User.objects.find(pk)
    data = User.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getInfo(request):
    post = json.loads(request.body)
    pk = post.get('id')
    good = User.objects.find(pk)
    data = User.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'user': data,
            'perms': [1000,1001,1002,1003],
            'market': [1]
        }
    }
    return JsonResponse(response)

@require_POST
def getByPhone(request):
    post = json.loads(request.body)
    phone = post.get('phone')
    good = User.objects.getByPhone(phone)
    data = User.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    goods = User.objects.getList(company_id, page, num)
    data = User.objects.encoderList(goods)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)
