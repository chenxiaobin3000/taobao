from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 订单表
class Order(models.Model):
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 应付
    actual_pay = models.DecimalField(max_digits=10, decimal_places=2) # 实际付款
    procure_pay = models.DecimalField(max_digits=10, decimal_places=2) # 采购付款
    order_status = models.IntegerField(db_index=True) # 状态
    create_time = models.DateTimeField(db_index=True) # 创建时间
    product_name = models.CharField(max_length=1024) # 商品名称
    order_note = models.CharField(max_length=1024) # 订单备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_order'
