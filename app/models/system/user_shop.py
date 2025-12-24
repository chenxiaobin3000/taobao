from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 用户-店铺关系表
class UserShopManager(models.Manager):
    def add(self, user_id, shop_id):
        # 无论如何都先删除，肯定不会有重复的
        self.filter(user_id=user_id, shop_id=shop_id).delete()
        return self.create(user_id=user_id, shop_id=shop_id)

    def delete(self, user_id, shop_id):
        return self.filter(user_id=user_id, shop_id=shop_id).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getList(self, user_id):
        return self.filter(user_id=user_id)

    def encoder(self, userShop):
        return model_to_dict(userShop, fields=['id', 'user_id', 'shop_id'])

    def encoderList(self, userShops):
        return [model_to_dict(userShop, fields=['id', 'user_id', 'shop_id']) for userShop in userShops]
    
class UserShop(models.Model):
    objects = UserShopManager()
    user_id = models.IntegerField(db_index = True) # 用户id
    shop_id = models.IntegerField(db_index = True) # 店铺
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_user_shop'
