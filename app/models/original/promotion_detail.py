from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 推广明细表
class PromotionDetailManager(models.Manager):
    def add(self, shop_id, promotion_date, good_id, show_num, click_num, click_rate, cost, average_cost, thousand_cost, deal_amount, deal_num, deal_cost, shop_cart, favorites, roi):
        return self.create(shop_id=shop_id, promotion_date=promotion_date, good_id=good_id, show_num=show_num, click_num=click_num, click_rate=click_rate, cost=cost, average_cost=average_cost, thousand_cost=thousand_cost, deal_amount=deal_amount, deal_num=deal_num, deal_cost=deal_cost, shop_cart=shop_cart, favorites=favorites, roi=roi)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByIdAndDate(self, shop_id, promotion_date, good_id):
        return self.filter(shop_id=shop_id, promotion_date=promotion_date, good_id=good_id).first()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id).order_by('-promotion_date')[left:right]

    def encoder(self, promotion):
        if promotion:
            return model_to_dict(promotion, fields=['id', 'shop_id', 'promotion_date', 'good_id', 'show_num', 'click_num', 'click_rate', 'cost', 'average_cost', 'thousand_cost', 'deal_amount', 'deal_num', 'deal_cost', 'shop_cart', 'favorites', 'roi'])
        return None

    def encoderList(self, promotions):
        if promotions:
            return [model_to_dict(promotion, fields=['id', 'shop_id', 'promotion_date', 'good_id', 'show_num', 'click_num', 'click_rate', 'cost', 'average_cost', 'thousand_cost', 'deal_amount', 'deal_num', 'deal_cost', 'shop_cart', 'favorites', 'roi']) for promotion in promotions]
        return None

class PromotionDetail(models.Model):
    objects = PromotionDetailManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    promotion_date = models.DateField(db_index=True) # 推广日期
    good_id = models.CharField(max_length=20, db_index=True) # 商品id
    show_num = models.IntegerField(db_index=True) # 展现量
    click_num = models.IntegerField(db_index=True) # 点击量
    click_rate = models.DecimalField(max_digits=8, decimal_places=2) # 点击率
    cost = models.DecimalField(max_digits=8, decimal_places=2) # 花费
    average_cost = models.DecimalField(max_digits=8, decimal_places=2) # 平均花费
    thousand_cost = models.DecimalField(max_digits=8, decimal_places=2) # 千次花费
    deal_amount = models.DecimalField(max_digits=8, decimal_places=2) # 成交金额
    deal_num = models.IntegerField(db_index=True) # 成交笔数
    deal_cost = models.DecimalField(max_digits=8, decimal_places=2) # 成交成本
    shop_cart = models.IntegerField(db_index=True) # 购物车
    favorites = models.IntegerField(db_index=True) # 收藏数
    roi = models.DecimalField(max_digits=6, decimal_places=2) # 投产比
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_promotion_detail'
