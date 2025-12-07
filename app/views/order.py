from django.views.decorators.http import require_POST
from django.http import JsonResponse
from app.models import order

@require_POST
def addOrder(request):
    response = {}
    response['a'] = order.objects.get(id=1)
    return JsonResponse(response)
