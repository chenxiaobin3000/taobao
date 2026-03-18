from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict
from app.models.report.order import Order

# 订单汇总表
class OrderSummaryManager(models.Manager):
    def add(self, shop_id, order_id, payment, refund_customer, refund_platform, procure, refund_procure, transfer, order_status, create_time, good_ids, deduction, deduction_detail):
        return self.create(shop_id=shop_id, order_id=order_id, payment=payment, refund_customer=refund_customer, refund_platform=refund_platform, procure=procure, refund_procure=refund_procure, transfer=transfer, order_status=order_status, create_time=create_time, good_ids=good_ids, deduction=deduction, deduction_detail=deduction_detail)

    def set(self, pk, payment, refund_customer, refund_platform, procure, refund_procure, transfer, order_status, create_time, good_ids, deduction, deduction_detail):
        order = self.get(pk=pk)
        order.payment = payment
        order.refund_customer = refund_customer
        order.refund_platform = refund_platform
        order.procure = procure
        order.refund_procure = refund_procure
        order.transfer = transfer
        order.order_status = order_status
        order.create_time = create_time
        order.good_ids = good_ids
        order.deduction = deduction
        order.deduction_detail = deduction_detail
        return order.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getById(self, shop_id, order_id):
        return self.encoder(self.filter(shop_id=shop_id, order_id=order_id).first())

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-create_time')[left:right])

    def getAll(self, shop_id, order_status, start_date, end_date):
        return Order().total(shop_id, order_status, start_date, end_date)

    def encoder(self, order):
        if order:
            return model_to_dict(order, fields=['id', 'shop_id', 'order_id', 'payment', 'refund_customer', 'refund_platform', 'procure', 'refund_procure', 'transfer', 'order_status', 'create_time', 'good_ids', 'deduction', 'deduction_detail'])
        return None

    def encoderList(self, ordera):
        if ordera:
            return [model_to_dict(order, fields=['id', 'shop_id', 'order_id', 'payment', 'refund_customer', 'refund_platform', 'procure', 'refund_procure', 'transfer', 'order_status', 'create_time', 'good_ids', 'deduction', 'deduction_detail']) for order in ordera]
        return None

class OrderSummary(models.Model):
    objects = OrderSummaryManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 付款金额
    refund_customer = models.DecimalField(max_digits=10, decimal_places=2) # 给用户退款
    refund_platform = models.DecimalField(max_digits=10, decimal_places=2) # 给平台退款
    procure = models.DecimalField(max_digits=10, decimal_places=2) # 采购金额
    refund_procure = models.DecimalField(max_digits=10, decimal_places=2) # 采购退款
    transfer = models.DecimalField(max_digits=10, decimal_places=2) # 打款金额
    order_status = models.IntegerField(db_index=True) # 状态
    create_time = models.DateTimeField(db_index=True) # 创建时间
    good_ids = models.CharField(max_length=256) # 商品id列表，|分割
    deduction = models.DecimalField(max_digits=10, decimal_places=2) # 扣款金额
    deduction_detail = models.CharField(max_length=64) # 扣款明细
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_order_summary'
