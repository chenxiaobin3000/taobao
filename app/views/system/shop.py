import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.shop import Shop
from app.models.system.user import User
from app.models.system.user_shop import UserShop
from app.models.system.market import Market
from app.models.system.good import Good

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    market_id = int(post.get('mid'))
    name = post.get('name')
    deposit = int(post.get('deposit'))
    Shop.objects.add(company_id, market_id, name, deposit)
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
    name = post.get('name')
    deposit = int(post.get('deposit'))
    Shop.objects.set(pk, name, deposit)
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
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 存在商品不能删除
    good = Good.objects.getList(pk, 1, 1)
    if good:
        response['code'] = -1
        response['msg'] = '存在商品，不能删除'
        return JsonResponse(response, encoder=MyJSONEncoder)

    # 存在管理员不能删除
    shop = UserShop.objects.getListByShop(pk)
    if shop:
        response['code'] = -1
        response['msg'] = '存在管理员，不能删除'
        return JsonResponse(response, encoder=MyJSONEncoder)

    Shop.objects.delete(pk)
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    company_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Shop.objects.total(company_id)
    shops = Shop.objects.getList(company_id, page, num)

    # 所有用户信息
    users = User.objects.getList(company_id, 1, 1000)

    # 获取平台、管理员信息
    for data in shops:
        market = Market.objects.find(data['market_id'])
        data['market_name'] = market['name']

        userShops = UserShop.objects.getListByShop(data['id'])
        if not userShops:
            continue
        for userShop in userShops:
            del userShop['id']
            del userShop['shop_id']
            for user in users:
                if user['id'] == userShop['user_id']:
                    userShop['name'] = user['name']
                    break
        data['users'] = userShops

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': shops
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getOwnList(request):
    post = json.loads(request.body)
    company_id = int(post.get('id'))
    user_id = int(post.get('uid'))
    shops = Shop.objects.getList(company_id, 1, 1000)
    userShops = UserShop.objects.getList(user_id, 1, 1000)
    datas = []

    # 获取平台、管理员信息
    if userShops:
        for data in shops:
            for userShop in userShops:
                if data['id'] == userShop['shop_id']:
                    datas.append(data)
                    break

    response = {
        'code': 0,
        'msg': 'success',
        'data': datas
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
