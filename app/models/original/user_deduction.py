from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 扣费表
class UserDeductionManager(models.Manager):
    def add(self, user_id, shop_id, order_id, amount, amount_type, create_time, deduction_note):
        return self.create(user_id=user_id, shop_id=shop_id, order_id=order_id, amount=amount, amount_type=amount_type, create_time=create_time, deduction_note=deduction_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByCTime(self, user_id, shop_id, order_id, amount_type, create_time):
        return self.encoder(self.filter(user_id=user_id, shop_id=shop_id, order_id=order_id, amount_type=amount_type, create_time=create_time).first())

    def total(self, user_id, shop_id):
        return self.filter(user_id=user_id, shop_id=shop_id).count()

    def getList(self, user_id, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(user_id=user_id, shop_id=shop_id).order_by('-create_time')[left:right])

    def encoder(self, deduction):
        if deduction:
            return model_to_dict(deduction, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'deduction_note'])
        return None

    def encoderList(self, deductions):
        if deductions:
            return [model_to_dict(deduction, fields=['id', 'order_id', 'amount', 'amount_type', 'create_time', 'deduction_note']) for deduction in deductions]
        return None
    
class UserDeduction(models.Model):
    objects = UserDeductionManager()
    user_id = models.IntegerField(db_index = True) # 用户id
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    amount_type = models.IntegerField(db_index=True) # 扣费类型
    create_time = models.DateTimeField(db_index=True) # 创建时间
    deduction_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_user_eduction'
