from django.db import models
from django.utils import timezone

# 店铺表
class ShopManager(models.Manager):
    def add(self, user_id, name):
        return self.create(user_id=user_id, name=name)

    def set(self, pk, user_id, name):
        return self.filter(pk=pk).update(user_id=user_id, name=name)

    def delete(self, pk):
        return self.filter(pk=pk).delete()

    def get(self, pk):
        return self.filter(pk=pk)

    def getList(self, user_id):
        return self.filter(user_id=user_id)
    
class Shop(models.Model):
    objects = ShopManager()
    user_id = models.IntegerField(db_index = True) # 归属用户id
    name = models.CharField(max_length = 16, db_index = True, unique = True) # 店铺名称
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_Shop'
