from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 聚合支付表 - 废弃数据
class PolymerizeDiscardManager(models.Manager):
    def add(self, shop_id, order_id, amount, amount_type, create_time, polymerize_note):
        return self.create(shop_id=shop_id, order_id=order_id, amount=amount, amount_type=amount_type, create_time=create_time, polymerize_note=polymerize_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def deleteAll(self, shop_id):
        return self.filter(shop_id=shop_id).delete()

    def getByCTime(self, shop_id, order_id, amount_type, create_time):
        return self.filter(shop_id=shop_id, order_id=order_id, amount_type=amount_type, create_time=create_time).first()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id).order_by('-create_time')[left:right]

    def encoder(self, polymerize):
        if polymerize:
            return model_to_dict(polymerize, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'polymerize_note'])
        return None

    def encoderList(self, polymerizes):
        if polymerizes:
            return [model_to_dict(polymerize, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'polymerize_note']) for polymerize in polymerizes]
        return None
    
    
class PolymerizeDiscard(models.Model):
    objects = PolymerizeDiscardManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    amount_type = models.IntegerField(db_index=True) # 扣费类型
    create_time = models.DateTimeField(db_index=True) # 创建时间
    polymerize_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_polymerize_discard'
