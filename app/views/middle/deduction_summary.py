import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.deduction_summary import DeductionSummary

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    start_date = post.get('cdate')

    # 获取当前日期

    # 从最后一天开始生成刷单信息
        # 不存在的就插入

    order_id = 0
    amount = 0
    deduction_detail = ''
    DeductionSummary.objects.add(shop_id, order_id, amount, deduction_detail)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = FakeSummary.objects.total()
    fakes = FakeSummary.objects.getList(shop_id, page, num)
    data = FakeSummary.objects.encoderList(fakes)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': data
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
