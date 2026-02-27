from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 退货表
class UserRefundManager(models.Manager):
    def add(self, user_id, shop_id, refund_id, order_id, product_id, actual_pay, refund_pay, refund_platform, refund_type, refund_status, pay_time, apply_time, timeout_time, complete_time):
        return self.create(user_id=user_id, shop_id=shop_id, refund_id=refund_id, order_id=order_id, product_id=product_id, actual_pay=actual_pay, refund_pay=refund_pay, refund_platform=refund_platform, refund_type=refund_type, refund_status=refund_status, pay_time=pay_time, apply_time=apply_time, timeout_time=timeout_time, complete_time=complete_time)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByIdAndTime(self, user_id, shop_id, order_id, refund_id, product_id, apply_time):
        return self.encoder(self.filter(user_id=user_id, shop_id=shop_id, order_id=order_id, refund_id=refund_id, product_id=product_id, apply_time=apply_time).first())

    def total(self, user_id, shop_id):
        return self.filter(user_id=user_id, shop_id=shop_id).count()

    def getList(self, user_id, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(user_id=user_id, shop_id=shop_id).order_by('-apply_time')[left:right])

    def encoder(self, refund):
        if refund:
            return model_to_dict(refund, fields=['id', 'shop_id', 'refund_id', 'order_id', 'product_id', 'actual_pay', 'refund_pay', 'refund_platform', 'refund_type', 'refund_status', 'pay_time', 'apply_time', 'timeout_time', 'complete_time'])
        return None

    def encoderList(self, refunds):
        if refunds:
            return [model_to_dict(refund, fields=['id', 'shop_id', 'refund_id', 'order_id', 'product_id', 'actual_pay', 'refund_pay', 'refund_platform', 'refund_type', 'refund_status', 'pay_time', 'apply_time', 'timeout_time', 'complete_time']) for refund in refunds]
        return None
    
class UserRefund(models.Model):
    objects = UserRefundManager()
    user_id = models.IntegerField(db_index = True) # 用户id
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    refund_id = models.CharField(max_length=20) # 退款id
    product_id = models.CharField(max_length=20, db_index=True) # 商品id
    actual_pay = models.DecimalField(max_digits=10, decimal_places=2) # 实际付款
    refund_pay = models.DecimalField(max_digits=10, decimal_places=2) # 退客户金额
    refund_platform = models.DecimalField(max_digits=10, decimal_places=2) # 退平台金额
    refund_type = models.IntegerField(db_index=True) # 退货类型
    refund_status = models.IntegerField(db_index=True) # 退货状态
    pay_time = models.DateTimeField(db_index=True) # 支付时间
    apply_time = models.DateTimeField(db_index=True) # 申请时间
    timeout_time = models.DateTimeField() # 超时时间
    complete_time = models.DateTimeField() # 完结时间
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_user_refund'
