from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models import order

@require_POST
def addOrder(request):
    response = {
        'code': 0,
        'msg': 'success',
        'data': {}
    }
    return JsonResponse(response)
