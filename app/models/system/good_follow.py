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

    def getByGood(self, shop_id, good_id):
        return self.encoder(self.filter(shop_id=shop_id, good_id=good_id).first())

    def getGoodIds(self, shop_id):
        return list(self.filter(shop_id=shop_id).values_list('good_id', flat=True))

    def getPriorityMap(self, shop_id):
        return {follow.good_id: follow.priority for follow in self.filter(shop_id=shop_id)}

    def getAllByShop(self, shop_id):
        return self.encoderList(self.filter(shop_id=shop_id))

    def refreshPriority(self, shop_id, order_good_ids, promotion_good_ids):
        order_good_ids = set(order_good_ids)
        promotion_good_ids = set(promotion_good_ids)
        active_good_ids = order_good_ids | promotion_good_ids
        follows = {follow.good_id: follow for follow in self.filter(shop_id=shop_id)}
        for good_id in active_good_ids:
            if good_id in order_good_ids and good_id in promotion_good_ids:
                priority = 8
            elif good_id in order_good_ids:
                priority = 10
            else:
                priority = 6
            follow = follows.get(good_id)
            if follow:
                if follow.priority != priority:
                    follow.priority = priority
                    follow.save(update_fields=['priority'])
            else:
                self.add(shop_id, good_id, priority)
        for good_id, follow in follows.items():
            if good_id not in active_good_ids and follow.priority != 5:
                follow.priority = 5
                follow.save(update_fields=['priority'])

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-priority')[left:right])

    def encoder(self, good):
        if good:
            return model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'priority'])
        return None

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
