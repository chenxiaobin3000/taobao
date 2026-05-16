import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.omission import Omission
from app.views.common import success

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    start_date = post.get('sdate')
    end_date = post.get('edate')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    total = Omission.objects.total(shop_id, start_date, end_date)
    datas = Omission.objects.getList(shop_id, page, num, start_date, end_date)
    response = success({
            'total': total['id__count'],
            'amount': total['amount__sum'] if total['amount__sum'] else 0,
            'list': datas
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
