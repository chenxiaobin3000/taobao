import json
from datetime import datetime

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from app.json_encoder import MyJSONEncoder
from app.models.middle.good_prepare_record import GoodPrepareRecord
from app.views.common import failed, success


def parse_date(value):
    return datetime.strptime(value, '%Y-%m-%d').date()


@require_POST
@transaction.atomic
def set(request):
    post = json.loads(request.body)
    shop_ids = post.get('ids') or []
    prepare_date = post.get('cdate')
    prepare_detail = post.get('detail') or ''
    harvest_date = post.get('hdate') or None
    record_note = post.get('note') or ''
    if not shop_ids:
        return JsonResponse(failed('请选择店铺'), encoder=MyJSONEncoder)
    if not prepare_detail:
        return JsonResponse(failed('上新明细不能为空'), encoder=MyJSONEncoder)
    if len(prepare_detail) > 20:
        return JsonResponse(failed('上新明细不能超过20个字符'), encoder=MyJSONEncoder)
    if len(record_note) > 20:
        return JsonResponse(failed('备注不能超过20个字符'), encoder=MyJSONEncoder)
    if not GoodPrepareRecord.objects.set(
        request.user_id,
        shop_ids,
        prepare_date,
        prepare_detail,
        harvest_date,
        record_note
    ):
        return JsonResponse(failed('店铺不存在或无权限'), encoder=MyJSONEncoder)
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
@transaction.atomic
def clear(request):
    post = json.loads(request.body)
    shop_ids = post.get('ids') or []
    prepare_date = post.get('cdate')
    if not shop_ids:
        return JsonResponse(success(), encoder=MyJSONEncoder)
    if not GoodPrepareRecord.objects.clear(request.user_id, shop_ids, prepare_date):
        return JsonResponse(failed('店铺不存在或无权限'), encoder=MyJSONEncoder)
    return JsonResponse(success(), encoder=MyJSONEncoder)


@require_POST
def getList(request):
    post = json.loads(request.body)
    shop_id = int(post.get('id') or 0)
    start_date = parse_date(post.get('sdate'))
    end_date = parse_date(post.get('edate'))
    if start_date > end_date:
        return JsonResponse(failed('开始日期不能大于结束日期'), encoder=MyJSONEncoder)
    response = success({
        'list': GoodPrepareRecord.objects.getList(
            request.user_id,
            shop_id,
            start_date,
            end_date
        )
    })
    return JsonResponse(response, encoder=MyJSONEncoder)
