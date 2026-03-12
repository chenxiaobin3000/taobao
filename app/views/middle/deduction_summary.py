import json
from datetime import datetime
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.middle.deduction_summary import DeductionSummary
from app.models.trunk.deduction import Deduction
from app.models.trunk.polymerize import Polymerize

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    now_date = timezone.now()
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")

    # 计算开始日期至今的数据
    duration = now_date - start_date
    days = duration.days
    if days < 1:
        response['code'] = -1
        response['msg'] = '开始日期要早于当前时间'
        return JsonResponse(response, encoder=MyJSONEncoder)

    # 获取所有的扣费和聚合数据
    Deduction.objects.getAll(shop_id, start_date)
    Polymerize.objects.getAll(shop_id, start_date)

    # 已经存在，且金额一样就跳过
    order_id = 0
    amount = 0
    deduction_detail = ''
    DeductionSummary.objects.add(shop_id, order_id, amount, deduction_detail)

    response = {
        'code': 0,
        'msg': 'success'
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    page = int(post.get('page'))
    num = int(post.get('num'))
    total = DeductionSummary.objects.total(shop_id)
    fakes = DeductionSummary.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': fakes
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
