from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 推广明细表
class PromotionDetailManager(models.Manager):
    def add(self, shop_id, promotion_time, product_id, show_num, click_num, cost, average_cost, thousand_cost, deal_amount, deal_num, deal_cost, shop_cart, favorites, roi):
        return self.create(shop_id=shop_id, promotion_time=promotion_time, product_id=product_id, show_num=show_num, click_num=click_num, cost=cost, average_cost=average_cost, thousand_cost=thousand_cost, deal_amount=deal_amount, deal_num=deal_num, deal_cost=deal_cost, shop_cart=shop_cart, favorites=favorites, roi=roi)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self):
        return self.all().count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id).order_by('-promotion_time')[left:right]

    def encoder(self, promotion):
        return model_to_dict(promotion, fields=['id', 'shop_id', 'promotion_time', 'product_id', 'show_num', 'click_num', 'cost', 'average_cost', 'thousand_cost', 'deal_amount', 'deal_num', 'deal_cost', 'shop_cart', 'favorites', 'roi'])

    def encoderList(self, promotions):
        return [model_to_dict(promotion, fields=['id', 'shop_id', 'promotion_time', 'product_id', 'show_num', 'click_num', 'cost', 'average_cost', 'thousand_cost', 'deal_amount', 'deal_num', 'deal_cost', 'shop_cart', 'favorites', 'roi']) for promotion in promotions]

class PromotionDetail(models.Model):
    objects = PromotionDetailManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    promotion_time = models.DateTimeField(db_index=True) # 推广日期
    product_id = models.CharField(max_length=20, db_index=True) # 商品id
    show_num = models.IntegerField(db_index=True) # 展现量
    click_num = models.IntegerField(db_index=True) # 点击量
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
