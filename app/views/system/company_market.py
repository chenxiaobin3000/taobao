import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.company_market import CompanyMarket
from app.views.common import success

@require_POST
@transaction.atomic
def add(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    market_id = int(post.get('mid'))
    CompanyMarket.objects.add(company_id, market_id)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    CompanyMarket.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    company_id = int(post.get('cid'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = CompanyMarket.objects.total(company_id)
    cms = CompanyMarket.objects.getList(company_id, page, num)
    response = success({
            'total': total,
            'list': cms
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
