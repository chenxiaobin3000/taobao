import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.permission import Permission

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    role_id = int(post.get('rid'))
    p = int(post.get('pid'))
    Permission.objects.add(role_id, p)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    Permission.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    role_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Permission.objects.total(role_id)
    permissions = Permission.objects.getList(role_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': permissions
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
