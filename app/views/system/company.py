import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.company import Company

@require_POST
def add(request):
    post = json.loads(request.body)
    name = post.get('name')
    user_id = post.get('uid')
    company = Company.objects.add(name, user_id)
    data = Company.objects.encoder(company)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def set(request):
    post = json.loads(request.body)
    pk = post.get('id')
    name = post.get('name')
    user_id = post.get('uid')
    company = Company.objects.set(pk, name, user_id)
    data = Company.objects.encoder(company)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def delete(request):
    post = json.loads(request.body)
    pk = post.get('id')
    data = Company.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def get(request):
    post = json.loads(request.body)
    pk = post.get('id')
    company = Company.objects.find(pk)
    data = Company.objects.encoder(company)
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
    companys = Company.objects.getList(company_id, page, num)
    data = Company.objects.encoderList(companys)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': len(data),
            'list': data
        }
    }
    return JsonResponse(response)
