from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.user import User

@require_POST
def add(request):
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    company_id = request.POST.get('cid')
    role_id = request.POST.get('rid')
    user = User.objects.add(name, phone, company_id, role_id)
    data = User.objects.encoder(user)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def set(request):
    pk = request.POST.get('id')
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    company_id = request.POST.get('cid')
    role_id = request.POST.get('rid')
    data = User.objects.set(pk, name, phone, company_id, role_id)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def delete(request):
    pk = request.POST.get('id')
    data = User.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def get(request):
    pk = request.POST.get('id')
    good = User.objects.find(pk)
    data = User.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getInfo(request):
    pk = request.POST.get('id')
    good = User.objects.find(pk)
    data = User.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'user': data,
            'perms': [1000,1001,1002,1003],
            'market': [1]
        }
    }
    return JsonResponse(response)

@require_POST
def getByPhone(request):
    phone = request.POST.get('phone')
    good = User.objects.getByPhone(phone)
    data = User.objects.encoder(good)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    company_id = int(request.POST.get('cid'))
    page = int(request.POST.get('page'))
    num = int(request.POST.get('num'))
    goods = User.objects.getList(company_id, page, num)
    data = User.objects.encoderList(goods)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)
