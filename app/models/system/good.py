from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 商品表
class GoodManager(models.Manager):
    def add(self, shop_id, good_id, name, short_name, good_type, good_status):
        return self.create(shop_id=shop_id, good_id=good_id, name=name, short_name=short_name, good_type=good_type, good_status=good_status)

    def set(self, pk, name, short_name, good_status):
        good = self.get(pk=pk)
        good.name = name
        good.short_name = short_name
        good .good_status = good_status
        return good.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getById(self, shop_id, good_id):
        return self.filter(shop_id=shop_id, good_id=good_id).first()

    def getByName(self, shop_id, name):
        return self.filter(shop_id=shop_id, name=name).first()
    
    def getByType(self, shop_id, good_type):
        return self.filter(shop_id=shop_id, good_type=good_type)

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id)[left:right]

    def encoder(self, good):
        return model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name', 'good_type', 'good_status'])

    def encoderList(self, goods):
        return [model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name', 'good_type', 'good_status']) for good in goods]

class Good(models.Model):
    objects = GoodManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    good_id = models.CharField(max_length = 10, db_index = True) # 商品id
    name = models.CharField(max_length = 60, db_index = True) # 商品名称
    short_name = models.CharField(max_length = 16) # 商品短名
    good_type = models.IntegerField(db_index = True) # 商品类型
    good_status = models.IntegerField(db_index = True) # 商品状态
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good'
