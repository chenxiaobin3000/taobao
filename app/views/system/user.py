import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.user import User
from app.models.system.company import Company
from app.models.system.company_market import CompanyMarket
from app.models.system.market import Market
from app.models.system.shop import Shop
from app.models.system.user_shop import UserShop
from app.models.system.permission import Permission
from app.models.system.role import Role

@require_POST
@transaction.atomic
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
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    name = post.get('name')
    phone = post.get('phone')
    role_id = int(post.get('rid'))
    data = User.objects.set(pk, name, phone, role_id)
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
    data = User.objects.delete(pk)
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
    user = User.objects.find(pk)
    data = User.objects.encoder(user)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getInfo(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    user = User.objects.find(pk)
    dataUser = User.objects.encoder(user)

    # 公司信息
    company = Company.objects.find(user.company_id)
    dataCompany = Company.objects.encoder(company)

    # 平台信息
    companyMarkets = CompanyMarket.objects.getList(user.company_id, 1, 1000)
    dataCM = []
    for companyMarket in companyMarkets:
        market = Market.objects.find(companyMarket.market_id)
        tmp = Market.objects.encoder(market)
        dataCM.append(tmp)

    # 店铺信息
    dataShop = []
    userShops = UserShop.objects.getList(user.id, 1, 1000)
    for userShop in userShops:
        shop = Shop.objects.find(userShop.shop_id)
        tmp = Shop.objects.encoder(shop)
        del tmp['company_id']
        dataShop.append(tmp)

    # 权限信息
    permissions = Permission.objects.getList(user.role_id, 1, 1000)
    dataP = Permission.objects.encoderList(permissions)
    dataP = [data['permission'] for data in dataP]

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'user': dataUser,
            'company': dataCompany,
            'market': dataCM,
            'shop': dataShop,
            'perms': dataP
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getByPhone(request):
    post = json.loads(request.body)
    phone = post.get('phone')
    user = User.objects.getByPhone(phone)
    data = User.objects.encoder(user)
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
    company_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = User.objects.total(company_id)
    users = User.objects.getList(company_id, page, num)
    data = User.objects.encoderList(users)

    # 获取店铺、角色信息
    for user in data:
        user['shops'] = []
        userShops = UserShop.objects.getList(user['id'], 1, 1000)
        for userShop in userShops:
            shop = Shop.objects.find(userShop.shop_id)
            dataShop = Shop.objects.encoder(shop)
            user['shops'].append(dataShop)

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
