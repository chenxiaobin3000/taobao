from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 用户-店铺关系表
class UserShopManager(models.Manager):
    def add(self, user_id, shop_id):
        return self.create(user_id=user_id, shop_id=shop_id)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getList(self, user_id):
        return self.filter(user_id=user_id)

    def encoder(self, user_shop):
        return model_to_dict(user_shop, fields=['id', 'user_id', 'shop_id'])

    def encoderList(self, user_shops):
        return [model_to_dict(user_shop, fields=['id', 'user_id', 'shop_id']) for user_shop in user_shops]
    
class UserShop(models.Model):
    objects = UserShopManager()
    user_id = models.IntegerField(db_index = True) # 用户id
    shop_id = models.IntegerField(db_index = True) # 店铺
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_user_shop'
