from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 日报汇总表
class DaySummaryManager(models.Manager):
    def add(self, shop_id, create_date, payment, refund_customer, refund_platform, procure, refund_procure, transfer, deduction):
        return self.create(shop_id=shop_id, create_date=create_date, payment=payment, refund_customer=refund_customer, refund_platform=refund_platform, procure=procure, refund_procure=refund_procure, transfer=transfer, deduction=deduction)

    def set(self, pk, payment, refund_customer, refund_platform, procure, refund_procure, transfer, deduction):
        order = self.get(pk=pk)
        order.payment = payment
        order.refund_customer = refund_customer
        order.refund_platform = refund_platform
        order.procure = procure
        order.refund_procure = refund_procure
        order.transfer = transfer
        order.deduction = deduction
        return order.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-create_date')[left:right])

    def encoder(self, order):
        if order:
            return model_to_dict(order, fields=['id', 'shop_id', 'create_date', 'payment', 'refund_customer', 'refund_platform', 'procure', 'refund_procure', 'transfer', 'deduction'])
        return None

    def encoderList(self, ordera):
        if ordera:
            return [model_to_dict(order, fields=['id', 'shop_id', 'create_date', 'payment', 'refund_customer', 'refund_platform', 'procure', 'refund_procure', 'transfer', 'deduction']) for order in ordera]
        return None

class DaySummary(models.Model):
    objects = DaySummaryManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 交易日期
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 付款金额
    refund_customer = models.DecimalField(max_digits=10, decimal_places=2) # 给用户退款
    refund_platform = models.DecimalField(max_digits=10, decimal_places=2) # 给平台退款
    procure = models.DecimalField(max_digits=10, decimal_places=2) # 采购金额
    refund_procure = models.DecimalField(max_digits=10, decimal_places=2) # 采购退款
    transfer = models.DecimalField(max_digits=10, decimal_places=2) # 打款金额
    deduction = models.DecimalField(max_digits=10, decimal_places=2) # 扣款金额
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_day_summary'
