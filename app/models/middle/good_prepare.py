from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 预备商品表
class GoodPrepareManager(models.Manager):
    def add(self, shop_id, name, origin, origin_type, stock, stock_type, good_note):
        return self.create(shop_id=shop_id, name=name, origin=origin, origin_type=origin_type, stock=stock, stock_type=stock_type, good_note=good_note)

    def setJoinDate(self, pk, join_date):
        good = self.get(pk=pk)
        good.join_date = join_date
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
            return [model_to_dict(good, fields=['id', 'shop_id', 'name', 'origin', 'origin_type', 'stock', 'stock_type', 'join_date', 'good_note', 'ctime']) for good in goods]
        return None

class GoodPrepare(models.Model):
    objects = GoodPrepareManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    name = models.CharField(max_length = 20, db_index = True) # 商品名称
    origin = models.CharField(max_length = 12, db_index = True) # 外部id
    origin_type = models.IntegerField() # 外部id类型
    stock = models.CharField(max_length = 12, db_index = True) # 进货id
    stock_type = models.IntegerField() # 进货id类型
    join_date = models.DateField(null=True, blank=True) # 加入商品库日期
    good_note = models.CharField(max_length=20) # 备注
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good_prepare'
