from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 商品表
class GoodManager(models.Manager):
    def add(self, shop_id, good_id, name, short_name, good_type, good_status, origin, origin_type):
        return self.create(shop_id=shop_id, good_id=good_id, name=name, short_name=short_name, good_type=good_type, good_status=good_status, origin=origin, origin_type=origin_type)

    def set(self, pk, name, short_name, good_type, good_status, origin, origin_type):
        good = self.get(pk=pk)
        good.name = name
        good.short_name = short_name
        good.good_type = good_type
        good.good_status = good_status
        good.origin = origin
        good.origin_type = origin_type
        return good.save()

    def setFakeDate(self, pk, fake_date):
        good = self.get(pk=pk)
        good.fake_date = fake_date
        return good.save()

    def setPromotionDate(self, pk, promotion_date):
        good = self.get(pk=pk)
        good.promotion_date = promotion_date
        return good.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.encoder(self.get(pk=pk))

    def getById(self, shop_id, good_id):
        return self.encoder(self.filter(shop_id=shop_id, good_id=good_id).first())

    def getByName(self, shop_id, name):
        return self.encoder(self.filter(shop_id=shop_id, name=name).first())

    def getByOrigin(self, shop_id, origin):
        return self.encoder(self.filter(shop_id=shop_id, origin=origin).first())

    def getByType(self, shop_id, good_type):
        return self.encoderList(self.filter(shop_id=shop_id, good_type=good_type))

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-ctime')[left:right])

    def encoder(self, good):
        if good:
            return model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name', 'good_type', 'good_status', 'origin', 'origin_type', 'fake_date', 'promotion_date', 'ctime'])
        return None

    def encoderList(self, goods):
        if goods:
            return [model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name', 'good_type', 'good_status', 'origin', 'origin_type', 'fake_date', 'promotion_date', 'ctime']) for good in goods]
        return None

class Good(models.Model):
    objects = GoodManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    good_id = models.CharField(max_length = 10, db_index = True) # 商品id
    name = models.CharField(max_length = 60, db_index = True) # 商品名称
    short_name = models.CharField(max_length = 16) # 商品短名
    good_type = models.IntegerField(db_index = True) # 商品类型
    good_status = models.IntegerField(db_index = True) # 商品状态
    origin = models.CharField(max_length = 12, db_index = True) # 外部id
    origin_type = models.IntegerField() # 外部id类型
    fake_date = models.DateField(null=True, blank=True) # 首次刷单日期
    promotion_date = models.DateField(null=True, blank=True) # 首次刷单日期
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good'
