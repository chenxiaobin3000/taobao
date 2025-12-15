from django.db import models
from django.utils import timezone

# 商品表
class GoodManager(models.Manager):
    def add(self, shop_id, good_id, name):
        return self.create(shop_id=shop_id, good_id=good_id, name=name)

    def set(self, pk, shop_id, good_id, name):
        return self.filter(pk=pk).update(shop_id=shop_id, good_id=good_id, name=name)

    def delete(self, pk):
        return self.filter(pk=pk).delete()

    def get(self, pk):
        return self.filter(pk=pk)

    def getList(self, shop_id):
        return self.filter(shop_id=shop_id)

class Good(models.Model):
    objects = GoodManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    good_id = models.CharField(max_length = 10, db_index = True, unique = True) # 商品id
    name = models.CharField(max_length = 60, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good'
