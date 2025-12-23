import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.user_shop import UserShop

@require_POST
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
    return JsonResponse(response)

@require_POST
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = UserShop.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    post = json.loads(request.body)
    role_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    userShops = UserShop.objects.getList(role_id, page, num)
    data = UserShop.objects.encoderList(userShops)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
