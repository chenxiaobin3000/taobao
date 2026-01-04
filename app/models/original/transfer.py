from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 小额打款表
class Transfer(models.Model):
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 应付
    actual_pay = models.DecimalField(max_digits=10, decimal_places=2) # 实际付款
    status = models.IntegerField(db_index=True) # 状态
    create_time = models.DateTimeField(db_index=True) # 创建时间
    name = models.CharField(max_length=60) # 商品名称
    note = models.CharField(max_length=255) # 商品备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_transfer'
