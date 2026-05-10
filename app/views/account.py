import json
import secrets

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.json_encoder import MyJSONEncoder
from app.models.account import Account
from app.models.const.default_password import DefaultPassword
from app.models.session import Session


def success(data=None):
    response = {
        'code': 0,
        'msg': 'success'
    }
    if data is not None:
        response['data'] = data
    return response


def failed(msg, code=-1):
    return {
        'code': code,
        'msg': msg,
        'data': {}
    }


@require_POST
@transaction.atomic
def register(request):
    post = json.loads(request.body)
    account = post.get('account')
    password = post.get('password')
    user_id = 0

    Account.objects.add(account, password, user_id)
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def login(request):
    post = json.loads(request.body)
    account = post.get('account')
    password = post.get('password')
    account_object = Account.objects.getByAccount(account)

    if not account_object or password != account_object['password']:
        return JsonResponse(failed('account or password error'), encoder=MyJSONEncoder)

    token = secrets.token_hex(16)
    Session.objects.add(account_object['id'], token)
    return JsonResponse(success({
        'id': account_object['user_id'],
        'token': token
    }), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def logout(request):
    token = getattr(request, 'auth_token', None) or request.headers.get('token')
    if token:
        Session.objects.deleteByToken(token)
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def setPassword(request):
    post = json.loads(request.body)
    pk = request.user_id
    old_password = post.get('oldp')
    new_password = post.get('newp')

    account = Account.objects.getByUserId(pk)
    if not account:
        return JsonResponse(failed('account not found'), encoder=MyJSONEncoder)

    if old_password != account['password']:
        return JsonResponse(failed('old password error'), encoder=MyJSONEncoder)

    Account.objects.set(account['id'], new_password)
    Session.objects.deleteByAccount(account['id'])
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def resetPassword(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))

    account = Account.objects.getByUserId(pk)
    if not account:
        return JsonResponse(failed('account not found'), encoder=MyJSONEncoder)

    Account.objects.set(account['id'], DefaultPassword.VALUE)
    Session.objects.deleteByAccount(account['id'])
    return JsonResponse(success(), encoder=MyJSONEncoder)
