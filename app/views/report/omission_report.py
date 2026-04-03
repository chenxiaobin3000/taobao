import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.omission import Omission

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = Omission.objects.total(shop_id)
    data = Omission.objects.getList(shop_id, page, num)

    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total['total'],
            'amount': total['amount'],
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
