from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 现存采购订单
class ExistPurchaseManager(models.Manager):
    def add(self, shop_id, purchase_id):
        return self.create(shop_id=shop_id, purchase_id=purchase_id)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-ctime')[left:right])

    def encoderList(self, purchases):
        if purchases:
            return [model_to_dict(purchase, fields=['id', 'shop_id', 'purchase_id']) for purchase in purchases]
        return None

class ExistPurchase(models.Model):
    objects = ExistPurchaseManager()
    shop_id = models.IntegerField(db_index=True) # 店铺id
    purchase_id = models.CharField(max_length=20, db_index=True) # 采购id
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_exist_purchase'
