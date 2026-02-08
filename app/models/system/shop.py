from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 店铺表
class ShopManager(models.Manager):
    def add(self, company_id, market_id, name, deposit):
        return self.create(company_id=company_id, market_id=market_id, name=name, deposit=deposit)

    def set(self, pk, name, deposit):
        shop = self.get(pk=pk)
        shop.name = name
        shop.deposit = deposit
        return shop.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.encoder(self.get(pk=pk))

    def total(self, company_id):
        return self.filter(company_id=company_id).count()

    def getList(self, company_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(company_id=company_id)[left:right])

    def encoder(self, shop):
        if shop:
            return model_to_dict(shop, fields=['id', 'company_id', 'market_id', 'name', 'deposit'])
        return None

    def encoderList(self, shops):
        if shops:
            return [model_to_dict(shop, fields=['id', 'company_id', 'market_id', 'name', 'deposit']) for shop in shops]
        return None
    
class Shop(models.Model):
    objects = ShopManager()
    company_id = models.IntegerField(db_index = True) # 归属公司id
    market_id = models.IntegerField(db_index = True) # 归属平台id
    name = models.CharField(max_length = 16, db_index = True, unique = True) # 店铺名称
    deposit = models.IntegerField() # 保证金
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_shop'
