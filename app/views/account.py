import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.account import Account

# 系统默认密码
default_password = '888888'

@require_POST
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
    return JsonResponse(response)

@require_POST
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
        response['msg'] = 'fail'
        return JsonResponse(response)
    response['data']['id'] = object.user_id

    # 刷新session信息
    # response['data']['token'] = ''
    return JsonResponse(response)

@require_POST
def logout(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    # 清除session信息
    
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
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
    return JsonResponse(response)

@require_POST
def resetPassword(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Account.objects.set(pk, default_password)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)
