from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.forms.models import model_to_dict
from app.models.const.good_follow import GoodFollowStatus

# 商品表
class GoodManager(models.Manager):
    def add(self, shop_id, good_id, name, short_name, good_type, good_status, origin, origin_type, stock, stock_type):
        return self.create(shop_id=shop_id, good_id=good_id, name=name, short_name=short_name, good_type=good_type, good_status=good_status, origin=origin, origin_type=origin_type, stock=stock, stock_type=stock_type)

    def set(self, pk, name, short_name, good_type, good_status, origin, origin_type, stock, stock_type):
        good = self.get(pk=pk)
        good.name = name
        good.short_name = short_name
        good.good_type = good_type
        good.good_status = good_status
        good.origin = origin
        good.origin_type = origin_type
        good.stock = stock
        good.stock_type = stock_type
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

    def filterBySearch(self, shop_id, search, good_type=None, good_status=None, follow=0, follow_ids=None):
        queryset = self.filter(shop_id=shop_id)
        if search:
            keyword = str(search).strip()
            if keyword:
                queryset = queryset.filter(
                    Q(short_name__icontains=keyword) |
                    Q(name__icontains=keyword) |
                    Q(good_id=keyword) |
                    Q(origin=keyword) |
                    Q(stock=keyword)
                )
        if good_type:
            queryset = queryset.filter(good_type=good_type)
        if good_status:
            queryset = queryset.filter(good_status=good_status)
        if follow == GoodFollowStatus.HAS_FOLLOW:
            queryset = queryset.filter(good_id__in=follow_ids or [])
        elif follow == GoodFollowStatus.NOT_FOLLOW and follow_ids:
            queryset = queryset.exclude(good_id__in=follow_ids)
        return queryset

    def total(self, shop_id, search=None, good_type=None, good_status=None, follow=0, follow_ids=None):
        return self.filterBySearch(shop_id, search, good_type, good_status, follow, follow_ids).count()

    def getList(self, shop_id, page, num, search=None, good_type=None, good_status=None, follow=0, follow_ids=None, follow_priority_map=None):
        left = (page - 1) * num
        right = page * num
        queryset = self.filterBySearch(shop_id, search, good_type, good_status, follow, follow_ids)
        if follow == GoodFollowStatus.HAS_FOLLOW:
            goods = list(queryset)
            follow_priority_map = follow_priority_map or {}
            goods.sort(key=lambda good: (follow_priority_map.get(good.good_id, 0), self.goodIdSortValue(good.good_id)), reverse=True)
            return self.encoderList(goods[left:right])
        return self.encoderList(queryset.order_by('-ctime')[left:right])

    def goodIdSortValue(self, good_id):
        try:
            return int(good_id)
        except (TypeError, ValueError):
            return 0

    def getAll(self, shop_id):
        return self.encoderList(self.filter(shop_id=shop_id).order_by('good_id'))

    def getListInIds(self, shop_id, ids, good_status=None):
        queryset = self.filter(shop_id=shop_id, good_id__in=ids)
        if good_status:
            queryset = queryset.filter(good_status=good_status)
        return self.encoderList(queryset.order_by('-ctime'))

    def getListNotInIds(self, shop_id, ids):
        return self.encoderList(self.filter(shop_id=shop_id).exclude(good_id__in=ids).order_by('-ctime'))

    def encoder(self, good):
        if good:
            return model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name', 'good_type', 'good_status', 'origin', 'origin_type', 'stock', 'stock_type', 'fake_date', 'promotion_date', 'ctime'])
        return None

    def encoderList(self, goods):
        if goods:
            return [model_to_dict(good, fields=['id', 'shop_id', 'good_id', 'name', 'short_name', 'good_type', 'good_status', 'origin', 'origin_type', 'stock', 'stock_type', 'fake_date', 'promotion_date', 'ctime']) for good in goods]
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
    stock = models.CharField(max_length = 12, db_index = True) # 进货id
    stock_type = models.IntegerField() # 进货id类型
    fake_date = models.DateField(null=True, blank=True) # 首次刷单日期
    promotion_date = models.DateField(null=True, blank=True) # 首次刷单日期
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_good'
