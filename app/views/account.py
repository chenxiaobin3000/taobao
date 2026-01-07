import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.account import Account

# 系统默认密码:888888
default_password = '21218cca77804d2ba1922c33e0151105'

@require_POST
@transaction.atomic
def register(request):
    post = json.loads(request.body)
    account = post.get('account')
    password = post.get('password')
    # 创建用户
    user_id = 0

    # 创建账号
    account = Account.objects.add(account, password, user_id)
    data = Account.objects.encoder(account)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def login(request):
    post = json.loads(request.body)
    account = post.get('account')
    password = post.get('password')
    object = Account.objects.getByAccount(account)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    
    # 校验密码
    if (password != object.password):
        response['code'] = -1
        response['msg'] = '密码不正确'
        return JsonResponse(response, encoder=MyJSONEncoder)
    response['data']['id'] = object.user_id

    # 刷新session信息
    # response['data']['token'] = ''
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def logout(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    # 清除session信息
    
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def setPassword(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    password = post.get('password')
    data = Account.objects.set(pk, password)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def resetPassword(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Account.objects.set(pk, default_password)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
