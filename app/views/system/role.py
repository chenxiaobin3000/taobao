import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.role import Role

@require_POST
def add(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    name = post.get('name')
    role = Role.objects.add(company_id, name)
    data = Role.objects.encoder(role)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    name = post.get('name')
    role = Role.objects.set(pk, name)
    data = Role.objects.encoder(role)
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
    data = Role.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def get(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    role = Role.objects.find(pk)
    data = Role.objects.encoder(role)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    post = json.loads(request.body)
    company_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    roles = Role.objects.getList(company_id, page, num)
    data = Role.objects.encoderList(roles)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
