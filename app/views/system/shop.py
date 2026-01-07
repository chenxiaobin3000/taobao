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
    shop = Shop.objects.add(company_id, market_id, name)
    data = Shop.objects.encoder(shop)
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
    data = Shop.objects.set(pk, name)
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
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
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

    data = Shop.objects.delete(pk)
    response['data'] = data
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def get(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    shop = Shop.objects.find(pk)
    data = Shop.objects.encoder(shop)

    # 平台信息
    market = Market.objects.find(data['market_id'])
    data['market_name'] = market.name

    # 所有用户信息
    users = User.objects.getList(data['company_id'], 1, 1000)
    userDatas = User.objects.encoderList(users)

    # 管理员信息
    userShops = UserShop.objects.getListByShop(data['id'])
    userShopDatas = UserShop.objects.encoderList(userShops)
    for userShop in userShopDatas:
        del userShop['id']
        del userShop['shop_id']
        for user in userDatas:
            if user['id'] == userShop['user_id']:
                userShop['name'] = user['name']
                break
    data['users'] = userShopDatas
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
    shops = Shop.objects.getList(company_id, page, num)
    datas = Shop.objects.encoderList(shops)

    # 所有用户信息
    users = User.objects.getList(company_id, 1, 1000)
    userDatas = User.objects.encoderList(users)

    # 获取平台、管理员信息
    for data in datas:
        market = Market.objects.find(data['market_id'])
        data['market_name'] = market.name

        userShops = UserShop.objects.getListByShop(data['id'])
        userShopDatas = UserShop.objects.encoderList(userShops)
        for userShop in userShopDatas:
            del userShop['id']
            del userShop['shop_id']
            for user in userDatas:
                if user['id'] == userShop['user_id']:
                    userShop['name'] = user['name']
                    break
        data['users'] = userShopDatas

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': datas
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
