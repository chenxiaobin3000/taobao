import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.models.system.permission import Permission

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    role_id = int(post.get('rid'))
    p = int(post.get('pid'))
    permission = Permission.objects.add(role_id, p)
    data = Permission.objects.encoder(permission)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    data = Permission.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    role_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    permissions = Permission.objects.getList(role_id, page, num)
    data = Permission.objects.encoderList(permissions)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
