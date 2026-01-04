from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 推广明细表
class PromotionDetail(models.Model):
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
