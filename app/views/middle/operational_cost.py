import json

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.json_encoder import MyJSONEncoder
from app.models.middle.operational_cost import OperationalCost
from app.views.common import failed, success


def validate_user(user_ids, user_id):
    if not OperationalCost.objects.isCompanyUser(user_ids, user_id):
        raise ValueError('负责人不属于当前公司')


@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    user_ids = OperationalCost.objects.getCompanyUserIds(request.user_id)
    user_id = int(post.get('uid'))
    try:
        validate_user(user_ids, user_id)
    except ValueError as exc:
        return JsonResponse(failed(str(exc)), encoder=MyJSONEncoder)
    OperationalCost.objects.add(
        post.get('cdate'),
        user_id,
        post.get('name'),
        post.get('amount'),
        post.get('note')
    )
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def addList(request):
    post = json.loads(request.body)
    user_ids = OperationalCost.objects.getCompanyUserIds(request.user_id)
    try:
        OperationalCost.objects.addDataList(user_ids, post.get('m') or [])
    except ValueError as exc:
        return JsonResponse(failed(str(exc)), encoder=MyJSONEncoder)
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    user_ids = OperationalCost.objects.getCompanyUserIds(request.user_id)
    pk = int(post.get('id'))
    user_id = int(post.get('uid'))
    if not OperationalCost.objects.existsByCompany(pk, user_ids):
        return JsonResponse(failed('运营成本不存在'), encoder=MyJSONEncoder)
    try:
        validate_user(user_ids, user_id)
    except ValueError as exc:
        return JsonResponse(failed(str(exc)), encoder=MyJSONEncoder)
    OperationalCost.objects.set(
        pk,
        post.get('cdate'),
        user_id,
        post.get('name'),
        post.get('amount'),
        post.get('note')
    )
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    user_ids = OperationalCost.objects.getCompanyUserIds(request.user_id)
    if not OperationalCost.objects.deleteByCompany(int(post.get('id')), user_ids):
        return JsonResponse(failed('运营成本不存在'), encoder=MyJSONEncoder)
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
def getList(request):
    post = json.loads(request.body)
    user_ids = OperationalCost.objects.getCompanyUserIds(request.user_id)
    page = int(post.get('page'))
    num = int(post.get('num'))
    response = success({
        'total': OperationalCost.objects.total(user_ids),
        'list': OperationalCost.objects.getList(user_ids, page, num)
    })
    return JsonResponse(response, encoder=MyJSONEncoder)
