from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 商品关注表
class GoodFollowManager(models.Manager):
    def add(self, shop_id, good_id, priority):
        return self.create(shop_id=shop_id, good_id=good_id, priority=priority)

    def set(self, pk, priority):
        good = self.get(pk=pk)
        good.priority = priority
        return good.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-ctime')[left:right])

    def encoderList(self, goods):
        if goods:
            return [model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'priority']) for good in goods]
        return None

class GoodFollow(models.Model):
    objects = GoodFollowManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    good_id = models.CharField(max_length = 10, db_index = True) # 商品id
    priority = models.IntegerField(db_index = True) # 优先级
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good_follow'
