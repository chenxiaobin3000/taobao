import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.user import User

@require_POST
@transaction.atomic
def get(request):
    post = json.loads(request.body)
    name = post.get('name')
    data = ''

    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
