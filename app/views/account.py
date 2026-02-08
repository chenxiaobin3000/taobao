import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.const.default_password import DefaultPassword
from app.models.account import Account

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
    response = {
        'code': 0,
        'msg': 'success'
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
    if (password != object['password']):
        response['code'] = -1
        response['msg'] = '密码不正确'
        return JsonResponse(response, encoder=MyJSONEncoder)
    response['data']['id'] = object['user_id']

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
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def setPassword(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    old_password = post.get('oldp')
    new_password = post.get('newp')
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 用户id转账号id
    account = Account.objects.getByUserId(pk)
    if not account:
        response['code'] = -1
        response['msg'] = '查询账号信息异常'
        return JsonResponse(response, encoder=MyJSONEncoder)

    if old_password != account['password']:
        response['code'] = -1
        response['msg'] = '原始密码错误'
        return JsonResponse(response, encoder=MyJSONEncoder)

    Account.objects.set(account['id'], new_password)
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def resetPassword(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    response = {
        'code': 0,
        'msg': 'success'
    }

    # 用户id转账号id
    account = Account.objects.getByUserId(pk)
    if not account:
        response['code'] = -1
        response['msg'] = '查询账号信息异常'
        return JsonResponse(response, encoder=MyJSONEncoder)

    Account.objects.set(pk, DefaultPassword.VALUE)
    return JsonResponse(response, encoder=MyJSONEncoder)
