from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 推广表
class PromotionManager(models.Manager):
    def add(self, shop_id, create_date, payment, promotion_type, promotion_note):
        return self.create(shop_id=shop_id, create_date=create_date, payment=payment, promotion_type=promotion_type, promotion_note=promotion_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByDate(self, shop_id, create_date, promotion_type):
        return self.encoder(self.filter(shop_id=shop_id, create_date=create_date, promotion_type=promotion_type).first())

    def filterByDate(self, shop_id, start_date=None, end_date=None):
        queryset = self.filter(shop_id=shop_id)
        if start_date:
            queryset = queryset.filter(create_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(create_date__lte=end_date)
        return queryset

    def total(self, shop_id, start_date=None, end_date=None):
        return self.filterByDate(shop_id, start_date, end_date).count()

    def getList(self, shop_id, page, num, start_date=None, end_date=None):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filterByDate(shop_id, start_date, end_date).order_by('-create_date')[left:right])

    def getListByDate(self, shop_id, create_date):
        return self.encoderList(self.filter(shop_id=shop_id, create_date=create_date))

    def encoder(self, promotion):
        if promotion:
            return model_to_dict(promotion, fields=['id', 'create_date', 'payment', 'promotion_type', 'promotion_note'])
        return None

    def encoderList(self, promotions):
        if promotions:
            return [model_to_dict(promotion, fields=['id', 'create_date', 'payment', 'promotion_type', 'promotion_note']) for promotion in promotions]
        return None
    
class Promotion(models.Model):
    objects = PromotionManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 交易日期
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    promotion_type = models.IntegerField(db_index = True) # 类型
    promotion_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_promotion'
