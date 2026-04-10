import json
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from django.utils import timezone
from app.json_encoder import MyJSONEncoder
from app.models.middle.fake_summary import FakeSummary
from app.models.trunk.fake import Fake
from app.models.system.good import Good

@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    response = {
        'code': 0,
        'msg': 'success'
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
        datas = Fake.objects.getListByDay(shop_id, start, end)
        if datas:
            count = 0
            payment = 0
            note = ''
            good_ids = []
            for data in datas:
                count += 1
                payment += data['payment']
                gids = data['good_ids'].split('|')
                for gid in gids:
                    if gid and not gid in good_ids:
                        good = Good.objects.getById(shop_id, gid)
                        if good:
                            note = note + good['short_name'] + ' | '
                            good_ids.append(gid)
            if len(note) > 3:
                note = note[:-3]

            find_object = FakeSummary.objects.getByDate(shop_id, start)
            if find_object:
                # 已经生成的判断是否需要修改
                if find_object['order_amount'] != payment or find_object['order_num'] != count:
                    FakeSummary.objects.fix(find_object['id'], payment, count, note)
            else:
                FakeSummary.objects.add(shop_id, start, payment, count, 0, 0, 0, 0, note)

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
def batch(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id'))
    start_date = datetime.strptime(post.get('sdate'), "%Y-%m-%d")
    response = {
        'code': 0,
        'msg': 'success'
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
        find_object = FakeSummary.objects.getByDate(shop_id, start)
        if find_object and find_object['commission'] < 0.01:
            FakeSummary.objects.batch(find_object['id'], find_object['order_amount'], find_object['order_num'], find_object['order_num'] * 3, find_object['order_num'] * 2)

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
