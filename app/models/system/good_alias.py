from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 商品别名表
class GoodAliasManager(models.Manager):
    def add(self, shop_id, good_id, name):
        return self.create(shop_id=shop_id, good_id=good_id, name=name)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def deleteById(self, shop_id, good_id):
        return self.filter(shop_id=shop_id, good_id=good_id).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getById(self, shop_id, good_id):
        return self.filter(shop_id=shop_id, good_id=good_id)

    def getByName(self, shop_id, name):
        return self.filter(shop_id=shop_id, name=name).first()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id)[left:right]

    def encoder(self, good):
        return model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name'])

    def encoderList(self, goods):
        return [model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name']) for good in goods]

class GoodAlias(models.Model):
    objects = GoodAliasManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    good_id = models.CharField(max_length = 10, db_index = True) # 商品id
    name = models.CharField(max_length = 60, db_index = True) # 商品别名
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good_alias'
