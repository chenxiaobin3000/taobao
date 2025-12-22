import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models.system.company_market import CompanyMarket

@require_POST
def add(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    market_id = int(post.get('mid'))
    cm = CompanyMarket.objects.add(company_id, market_id)
    data = CompanyMarket.objects.encoder(cm)
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
    data = CompanyMarket.objects.delete(pk)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)

@require_POST
def getList(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    cms = CompanyMarket.objects.getList(company_id, page, num)
    data = CompanyMarket.objects.encoderList(cms)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response)
