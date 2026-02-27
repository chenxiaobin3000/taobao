from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 推广表
class UserPromotionManager(models.Manager):
    def add(self, user_id, shop_id, create_date, payment, promotion_type, promotion_note):
        return self.create(user_id=user_id, shop_id=shop_id, create_date=create_date, payment=payment, promotion_type=promotion_type, promotion_note=promotion_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByCDate(self, user_id, shop_id, create_date, promotion_type):
        return self.encoder(self.filter(user_id=user_id, shop_id=shop_id, create_date=create_date, promotion_type=promotion_type).first())

    def total(self, user_id, shop_id):
        return self.filter(user_id=user_id, shop_id=shop_id).count()

    def getList(self, user_id, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(user_id=user_id, shop_id=shop_id).order_by('-create_date')[left:right])

    def encoder(self, promotion):
        if promotion:
            return model_to_dict(promotion, fields=['id', 'create_date', 'payment', 'promotion_type', 'promotion_note'])
        return None

    def encoderList(self, promotions):
        if promotions:
            return [model_to_dict(promotion, fields=['id', 'create_date', 'payment', 'promotion_type', 'promotion_note']) for promotion in promotions]
        return None
    
class UserPromotion(models.Model):
    objects = UserPromotionManager()
    user_id = models.IntegerField(db_index = True) # 用户id
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 交易日期
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    promotion_type = models.IntegerField(db_index = True) # 类型
    promotion_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_user_promotion'
