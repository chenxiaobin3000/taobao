from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 刷单表
class FakeManager(models.Manager):
    def add(self, shop_id, order_id, payment, procure, order_status, create_time, good_ids, procure_ids, order_note):
        return self.create(shop_id=shop_id, order_id=order_id, payment=payment, procure=procure, order_status=order_status, create_time=create_time, good_ids=good_ids, procure_ids=procure_ids, order_note=order_note)

    def set(self, pk, procure, order_status, procure_ids, order_note):
        order = self.get(pk=pk)
        order.procure = procure
        order.order_status = order_status
        order.procure_ids = procure_ids
        order.order_note = order_note
        return order.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.encoder(self.get(pk=pk))

    def getById(self, shop_id, order_id):
        return self.encoder(self.filter(shop_id=shop_id, order_id=order_id).first())

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-create_time')[left:right])

    def getListByDay(self, shop_id, start_date, end_date):
        ret = self.filter(shop_id=shop_id, create_time__range=(start_date, end_date)).annotate(amounts=models.Sum('payment'), nums=models.Count('id')).values('amounts', 'nums')
        print(ret)
        return ret

    def encoder(self, order):
        if order:
            return model_to_dict(order, fields=['id', 'order_id', 'payment', 'procure', 'order_status', 'create_time', 'good_ids', 'procure_ids', 'order_note'])
        return None

    def encoderList(self, orders):
        if orders:
            return [model_to_dict(order, fields=['id', 'order_id', 'payment', 'procure', 'order_status', 'create_time', 'good_ids', 'procure_ids', 'order_note']) for order in orders]
        return None
    
class Fake(models.Model):
    objects = FakeManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 应付
    procure = models.DecimalField(max_digits=10, decimal_places=2) # 采购金额
    order_status = models.IntegerField(db_index=True) # 状态
    create_time = models.DateTimeField(db_index=True) # 创建时间
    good_ids = models.CharField(max_length=256) # 商品id列表，|分割
    procure_ids = models.CharField(max_length=256) # 采购订单号，|分割
    order_note = models.CharField(max_length=256) # 订单备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_fake'
