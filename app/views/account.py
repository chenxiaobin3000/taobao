from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.account import Account

# 系统默认密码
default_password = '888888'

@require_POST
def register(request):
    account = request.POST.get('account')
    password = request.POST.get('password')
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
    print(request.POST)
    account = request.POST.get('account')
    password = request.POST.get('password')
    print(account)
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
    pk = request.POST.get('id')
    # 清除session信息
    
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)

@require_POST
def setPassword(request):
    pk = request.POST.get('id')
    password = request.POST.get('password')
    data = Account.objects.set(pk, password)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def resetPassword(request):
    pk = request.POST.get('id')
    data = Account.objects.set(pk, default_password)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)
