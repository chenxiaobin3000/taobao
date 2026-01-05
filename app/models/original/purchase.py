from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 采购表
class PurchaseManager(models.Manager):
    def add(self, shop_id, purchase_id, order_id, payment, freight, total, order_status, create_time, product_name, purchase_note):
        return self.create(shop_id=shop_id, purchase_id=purchase_id, order_id=order_id, payment=payment, freight=freight, total=total, order_status=order_status, create_time=create_time, product_name=product_name, purchase_note=purchase_note)

    def set(self, pk, order_status):
        purchase = self.get(pk=pk)
        purchase.order_status = order_status
        return purchase.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id)[left:right]

    def encoder(self, purchase):
        return model_to_dict(purchase, fields=['shop_id', 'purchase_id', 'order_id', 'payment', 'freight', 'total', 'order_status', 'create_time', 'product_name', 'purchase_note'])

    def encoderList(self, purchases):
        return [model_to_dict(purchase, fields=['shop_id', 'purchase_id', 'order_id', 'payment', 'freight', 'total', 'order_status', 'create_time', 'product_name', 'purchase_note']) for purchase in purchases]
    
class Purchase(models.Model):
    objects = PurchaseManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    purchase_id = models.CharField(max_length=20, db_index=True) # 采购id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    payment = models.DecimalField(max_digits=6, decimal_places=2) # 应付
    freight = models.DecimalField(max_digits=6, decimal_places=2) # 运费
    total = models.DecimalField(max_digits=6, decimal_places=2) # 应付
    order_status = models.IntegerField(db_index=True) # 状态
    create_time = models.DateTimeField(db_index=True) # 创建时间
    product_name = models.CharField(max_length=32) # 商品名称
    purchase_note = models.CharField(max_length=32) # 采购备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_purchase'
