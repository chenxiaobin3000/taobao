from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 店铺表
class ShopManager(models.Manager):
    def add(self, company_id, market_id, name):
        return self.create(company_id=company_id, market_id=market_id, name=name)

    def set(self, pk, name):
        shop = self.get(pk=pk)
        shop.name = name
        return shop.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self):
        return self.all().count()

    def getList(self, company_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(company_id=company_id)[left:right]

    def encoder(self, shop):
        return model_to_dict(shop, fields=['id', 'company_id', 'market_id', 'name'])

    def encoderList(self, shops):
        return [model_to_dict(shop, fields=['id', 'company_id', 'market_id', 'name']) for shop in shops]
    
class Shop(models.Model):
    objects = ShopManager()
    company_id = models.IntegerField(db_index = True) # 归属公司id
    market_id = models.IntegerField(db_index = True) # 归属平台id
    name = models.CharField(max_length = 16, db_index = True, unique = True) # 店铺名称
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_shop'
