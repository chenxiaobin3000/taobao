from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 订单表
class OrderManager(models.Manager):
    def add(self, shop_id, order_id, payment, actual_pay, procure_pay, order_status, create_time, product_name, order_note):
        return self.create(shop_id=shop_id, order_id=order_id, payment=payment, actual_pay=actual_pay, procure_pay=procure_pay, order_status=order_status, create_time=create_time, product_name=product_name, order_note=order_note)

    def set(self, pk, procure_pay, order_status, order_note):
        order = self.get(pk=pk)
        order.procure_pay = procure_pay
        order.order_status = order_status
        order.order_note = order_note
        return order.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id)[left:right]

    def encoder(self, order):
        return model_to_dict(order, fields=['order_id', 'payment', 'actual_pay', 'procure_pay', 'order_status', 'create_time', 'product_name', 'order_note'])

    def encoderList(self, orders):
        return [model_to_dict(order, fields=['order_id', 'payment', 'actual_pay', 'procure_pay', 'order_status', 'create_time', 'product_name', 'order_note']) for order in orders]
    
class Order(models.Model):
    objects = OrderManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
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
