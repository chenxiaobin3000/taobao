from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 推广表
class PromotionManager(models.Manager):
    def add(self, shop_id, create_date, payment, promotion_note):
        return self.create(shop_id=shop_id, create_date=create_date, payment=payment, promotion_note=promotion_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self):
        return self.all().count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id).order_by('-create_date')[left:right]

    def encoder(self, promotion):
        return model_to_dict(promotion, fields=['id', 'create_date', 'payment', 'promotion_note'])

    def encoderList(self, promotions):
        return [model_to_dict(promotion, fields=['id', 'create_date', 'payment', 'promotion_note']) for promotion in promotions]
    
class Promotion(models.Model):
    objects = PromotionManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 交易日期
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 应付
    promotion_note = models.CharField(max_length=1024) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_promotion'
