import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.user import User
from app.models.system.company import Company
from app.models.system.company_market import CompanyMarket
from app.models.system.permission import Permission
from app.models.system.role import Role

@require_POST
def add(request):
    post = json.loads(request.body)
    name = post.get('name')
    phone = post.get('phone')
    company_id = int(post.get('cid'))
    role_id = int(post.get('rid'))
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
    pk = int(post.get('id'))
    name = post.get('name')
    phone = post.get('phone')
    company_id = int(post.get('cid'))
    role_id = int(post.get('rid'))
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
    pk = int(post.get('id'))
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
    pk = int(post.get('id'))
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
    pk = int(post.get('id'))
    user = User.objects.find(pk)

    # 平台信息
    companyMarkets = CompanyMarket.objects.getList(user.company_id)

    # 权限信息
    permissions = Permission.objects.getList(user.role_id)

    dataUser = User.objects.encoder(user)
    dataCM = CompanyMarket.objects.encoderList(companyMarkets)
    dataCM = [data['market_id'] for data in dataCM]
    dataP = Permission.objects.encoderList(permissions)
    dataP = [data['permission'] for data in dataP]
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'user': dataUser,
            'market': dataCM,
            'perms': dataP
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
    company_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    users = User.objects.getList(company_id, page, num)
    data = User.objects.encoderList(users)

    # 获取公司、角色信息
    for user in data:
        company = Company.objects.find(user['company_id'])
        user['company'] = company.name
        role = Role.objects.find(user['role_id'])
        user['role'] = role.name

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
