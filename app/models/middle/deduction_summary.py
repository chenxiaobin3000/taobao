from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 扣费汇总表
class DeductionSummaryManager(models.Manager):
    def add(self, shop_id, order_id, amount, deduction_detail):
        return self.create(shop_id=shop_id, order_id=order_id, amount=amount, deduction_detail=deduction_detail)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getById(self, shop_id, order_id):
        return self.encoder(self.filter(shop_id=shop_id, order_id=order_id).first())

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-ctime')[left:right])

    def encoder(self, deduction):
        if deduction:
            return model_to_dict(deduction, fields=['id', 'order_id', 'amount', 'deduction_detail'])
        return None

    def encoderList(self, deductions):
        if deductions:
            return [model_to_dict(deduction, fields=['id', 'order_id', 'amount', 'deduction_detail']) for deduction in deductions]
        return None

class DeductionSummary(models.Model):
    objects = DeductionSummaryManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    deduction_detail = models.CharField(max_length=64) # 明细
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_deduction_summary'
