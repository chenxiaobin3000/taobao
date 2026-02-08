import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.middle.fake_summary import FakeSummary
from app.models.original.fake import Fake

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    response = {
        'code': 0,
        'msg': 'success',
        'data': None
    }

    # 计算开始日期至今的数据
    duration = timezone.now() - start_date
    days = duration.days
    if days < 1:
        response['code'] = -1
        response['msg'] = '开始日期要早于当前时间'
        return JsonResponse(response, encoder=MyJSONEncoder)

    # 按天生成数据
    for i in range(0, days):
        start = start_date + timedelta(days=i)
        end = start_date + timedelta(days=i+1)
        # 已经生成的就跳过
        if FakeSummary.objects.getByDate(shop_id, start):
            continue
        data = Fake.objects.getListByDay(shop_id, start, end)
        if data and data['payment__sum'] and data['id__count'] > 0:
            FakeSummary.objects.add(shop_id, start, data['payment__sum'], data['id__count'], 0, 0, 0, 0, '')

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
    total = FakeSummary.objects.total(shop_id)
    fakes = FakeSummary.objects.getList(shop_id, page, num)
    response = {
        'code': 0,
        'msg': 'success',
        'data': {
            'total': total,
            'list': fakes
        }
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
