import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.user_shop import UserShop

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    user_id = int(post.get('uid'))
    shop_id = int(post.get('sid'))
    userShop = UserShop.objects.add(user_id, shop_id)
    data = UserShop.objects.encoder(userShop)
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
    user_id = int(post.get('uid'))
    shop_id = int(post.get('sid'))
    data = UserShop.objects.delete(user_id, shop_id)
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
    user_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = UserShop.objects.total(user_id)
    userShops = UserShop.objects.getList(user_id, page, num)
    data = UserShop.objects.encoderList(userShops)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
