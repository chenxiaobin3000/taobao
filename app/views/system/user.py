import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.default_password import DefaultPassword
from app.models.account import Account
from app.models.system.user import User
from app.models.system.company import Company
from app.models.system.company_market import CompanyMarket
from app.models.system.market import Market
from app.models.system.shop import Shop
from app.models.system.user_shop import UserShop
from app.models.system.permission import Permission

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    account = post.get('account')
    name = post.get('name')
    phone = post.get('phone')
    company_id = int(post.get('cid'))
    role_id = int(post.get('rid'))
    response = {
        'code': 0,
        'msg': 'success'
    }

    user = User.objects.add(name, phone, company_id, role_id)
    if not user:
        response['code'] = -1
        response['msg'] = '创建用户失败'
        return JsonResponse(response, encoder=MyJSONEncoder)

    Account.objects.add(account, DefaultPassword.VALUE, user.id)
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    name = post.get('name')
    phone = post.get('phone')
    role_id = int(post.get('rid'))
    User.objects.set(pk, name, phone, role_id)
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
    User.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def get(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    user = User.objects.find(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': user
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getInfo(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    user = User.objects.find(pk)

    # 公司信息
    company = Company.objects.find(user['company_id'])

    # 平台信息
    companyMarkets = CompanyMarket.objects.getList(user['company_id'], 1, 1000)
    dataCM = []
    for companyMarket in companyMarkets:
        market = Market.objects.find(companyMarket['market_id'])
        dataCM.append(market)

    # 店铺信息
    dataShop = []
    userShops = UserShop.objects.getList(user['id'], 1, 1000)
    for userShop in userShops:
        shop = Shop.objects.find(userShop['shop_id'])
        del shop['company_id']
        dataShop.append(shop)

    # 权限信息
    permissions = Permission.objects.getList(user['role_id'], 1, 1000)
    permissions = [data['permission'] for data in permissions]

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'user': user,
            'company': company,
            'market': dataCM,
            'shop': dataShop,
            'perms': permissions
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getByPhone(request):
    post = json.loads(request.body)
    phone = post.get('phone')
    user = User.objects.getByPhone(phone)
    response = {
        'code': 0,
        'msg': 'success',
        'data': user
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
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }

    # 获取账号、店铺信息
    for user in users:
        account = Account.objects.getByUserId(user['id'])
        if not account:
            response['code'] = -1
            response['msg'] = '账号不存在'
        user['account'] = account['account']
        user['shops'] = []
        userShops = UserShop.objects.getList(user['id'], 1, 1000)
        if not userShops:
            continue
        for userShop in userShops:
            shop = Shop.objects.find(userShop['shop_id'])
            user['shops'].append(shop)

    response['data']['total'] = total
    response['data']['list'] = users
    return JsonResponse(response, encoder=MyJSONEncoder)
