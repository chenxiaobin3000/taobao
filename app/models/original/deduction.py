from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 扣费表
class DeductionManager(models.Manager):
    def add(self, shop_id, order_id, amount, amount_type, create_time, deduction_note):
        return self.create(shop_id=shop_id, order_id=order_id, amount=amount, amount_type=amount_type, create_time=create_time, deduction_note=deduction_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getByCTime(self, shop_id, order_id, amount_type, create_time):
        return self.filter(shop_id=shop_id, order_id=order_id, amount_type=amount_type, create_time=create_time).first()

    def total(self):
        return self.all().count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id).order_by('-create_time')[left:right]

    def encoder(self, deduction):
        return model_to_dict(deduction, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'deduction_note'])

    def encoderList(self, deductions):
        return [model_to_dict(deduction, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'deduction_note']) for deduction in deductions]
    
class Deduction(models.Model):
    objects = DeductionManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    amount_type = models.IntegerField(db_index=True) # 扣费类型
    create_time = models.DateTimeField(db_index=True) # 创建时间
    deduction_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_deduction'
