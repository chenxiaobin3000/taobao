from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 刷单表
class FakeManager(models.Manager):
    def add(self, shop_id, create_date, fake_amount, fake_num, commission, freight, fake_note):
        return self.create(shop_id=shop_id, create_date=create_date, fake_amount=fake_amount, fake_num=fake_num, commission=commission, freight=freight, fake_note=fake_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id)[left:right]

    def encoder(self, fake):
        return model_to_dict(fake, fields=['shop_id', 'create_date', 'fake_amount', 'fake_num', 'commission', 'freight', 'fake_note'])

    def encoderList(self, fakes):
        return [model_to_dict(fake, fields=['shop_id', 'create_date', 'fake_amount', 'fake_num', 'commission', 'freight', 'fake_note']) for fake in fakes]
    
class Fake(models.Model):
    objects = FakeManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 刷单日期
    fake_amount = models.IntegerField() # 刷单总金额
    fake_num = models.IntegerField() # 刷单订单数
    commission = models.DecimalField(max_digits=6, decimal_places=2) # 实际付款
    freight = models.DecimalField(max_digits=6, decimal_places=2) # 运费
    fake_note = models.CharField(max_length=32) # 刷单备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_fake'
