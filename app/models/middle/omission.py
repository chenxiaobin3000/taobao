from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 遗漏表
class OmissionManager(models.Manager):
    def add(self, shop_id, source, order_id, amount, create_time,  deduction_detail):
        return self.create(shop_id=shop_id, source=source, order_id=order_id, amount=amount, create_time=create_time, deduction_detail=deduction_detail)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def deleteByDate(self, shop_id, create_time):
        return self.filter(shop_id=shop_id, create_time__gte=create_time).delete()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).aggregate(models.Sum('amount'), models.Count('id'))

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-create_time')[left:right])

    def encoder(self, deduction):
        if deduction:
            return model_to_dict(deduction, fields=['id', 'shop_id', 'source', 'order_id', 'amount', 'create_time', 'deduction_detail'])
        return None

    def encoderList(self, deductions):
        if deductions:
            return [model_to_dict(deduction, fields=['id', 'shop_id', 'source', 'order_id', 'amount', 'create_time', 'deduction_detail']) for deduction in deductions]
        return None

class Omission(models.Model):
    objects = OmissionManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    source = models.IntegerField(db_index = True) # 来源
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    create_time = models.DateTimeField(db_index=True) # 创建时间
    deduction_detail = models.CharField(max_length=64) # 明细
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_omission'
