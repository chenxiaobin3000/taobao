import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.middle.fake_summary import FakeSummary

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))

    # 获取当前日期

    # 从最后一天开始生成刷单信息
        # 不存在的就插入

    create_date = post.get('cdate')
    order_amount = 0
    order_num = 0
    fake_amount = order_amount
    fake_num = order_num
    commission = 0
    freight = 0
    fake_note = ''
    FakeSummary.objects.add(shop_id, create_date, order_amount, order_num, fake_amount, fake_num, commission, freight, fake_note)

    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }
    return JsonResponse(response, encoder=MyJSONEncoder)

@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    pk = int(post.get('id'))
    fake_amount = post.get('amount')
    fake_num = int(post.get('num'))
    commission = int(post.get('comm'))
    freight = int(post.get('freight'))
    fake_note = post.get('note')
    data = FakeSummary.objects.set(pk, fake_amount, fake_num, commission, freight, fake_note)
    response = {
        'code': 0,
        'msg': 'success',
        'data': data
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
