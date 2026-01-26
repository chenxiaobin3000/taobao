import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from app.json_encoder import MyJSONEncoder
from app.models.system.user import User

# 刷新订单中间表
@require_POST
@transaction.atomic
def flush(request):
    post = json.loads(request.body)
    name = post.get('name')
    data = ''

    # 删除起始时间以后的所有数据

    # 从起始时间开始生成新数据

    response = {
        'code': 0,
        'msg': 'success',
        'data': data
    }
    return JsonResponse(response, encoder=MyJSONEncoder)
