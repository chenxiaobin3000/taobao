from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 退货表
class Refund(models.Model):
    refund_id = models.CharField(max_length=20, db_index=True) # 退款id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    product_id = models.CharField(max_length=20, db_index=True) # 商品id
    actual_pay = models.DecimalField(max_digits=10, decimal_places=2) # 实际付款
    refund_pay = models.DecimalField(max_digits=10, decimal_places=2) # 退款金额
    refund_type = models.IntegerField(db_index=True) # 退货类型
    refund_status = models.IntegerField(db_index=True) # 退货状态
    apply_time = models.DateTimeField(db_index=True) # 申请时间
    timeout_time = models.DateTimeField(db_index=True) # 超时时间
    complete_time = models.DateTimeField(db_index=True) # 完结时间
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_refund'
