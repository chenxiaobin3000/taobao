from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 聚合支付表 - 废弃数据
class UserPolymerizeDiscardManager(models.Manager):
    def add(self, user_id, shop_id, order_id, amount, amount_type, create_time, polymerize_note):
        return self.create(user_id=user_id, shop_id=shop_id, order_id=order_id, amount=amount, amount_type=amount_type, create_time=create_time, polymerize_note=polymerize_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def deleteAll(self, user_id, shop_id):
        return self.filter(user_id=user_id, shop_id=shop_id).delete()

    def getByCTime(self, user_id, shop_id, order_id, amount_type, create_time):
        return self.encoder(self.filter(user_id=user_id, shop_id=shop_id, order_id=order_id, amount_type=amount_type, create_time=create_time).first())

    def total(self, user_id, shop_id):
        return self.filter(user_id=user_id, shop_id=shop_id).count()

    def getList(self, user_id, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(user_id=user_id, shop_id=shop_id).order_by('-create_time')[left:right])

    def encoder(self, polymerize):
        if polymerize:
            return model_to_dict(polymerize, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'polymerize_note'])
        return None

    def encoderList(self, polymerizes):
        if polymerizes:
            return [model_to_dict(polymerize, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'polymerize_note']) for polymerize in polymerizes]
        return None
    
    
class UserPolymerizeDiscard(models.Model):
    objects = UserPolymerizeDiscardManager()
    user_id = models.IntegerField(db_index = True) # 用户id
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    amount_type = models.IntegerField(db_index=True) # 扣费类型
    create_time = models.DateTimeField(db_index=True) # 创建时间
    polymerize_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_user_polymerize_discard'
