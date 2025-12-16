from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 商品表
class GoodManager(models.Manager):
    def add(self, shop_id, good_id, name, short_name):
        return self.create(shop_id=shop_id, good_id=good_id, name=name, short_name=short_name)

    def set(self, pk, shop_id, good_id, name, short_name):
        good = self.get(pk=pk)
        good.shop_id = shop_id
        good.good_id = good_id
        good.name = name
        good.short_name = short_name
        return good.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id)[left:right]

    def encoder(self, good):
        return model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name'])

    def encoderList(self, goods):
        return [model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name']) for good in goods]

class Good(models.Model):
    objects = GoodManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    good_id = models.CharField(max_length = 10, db_index = True, unique = True) # 商品id
    name = models.CharField(max_length = 60, db_index = True, unique = True)
    short_name = models.CharField(max_length = 16, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good'
