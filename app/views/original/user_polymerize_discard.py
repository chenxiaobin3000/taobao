import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.original.user_polymerize_discard import UserPolymerizeDiscard
from app.views.common import success

@require_POST
@transaction.atomic
def delete(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    UserPolymerizeDiscard.objects.delete(pk)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def deleteAll(request):
    post = json.loads(request.body)
    id = int(post.get('id'))
    user_id = request.user_id
    UserPolymerizeDiscard.objects.deleteAll(user_id, id)
    response = success()
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    user_id = request.user_id
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = UserPolymerizeDiscard.objects.total(user_id, shop_id)
    polymerizes = UserPolymerizeDiscard.objects.getList(user_id, shop_id, page, num)
    response = success({
            'total': total,
            'list': polymerizes
        })
    return JsonResponse(response, encoder=MyJSONEncoder)
