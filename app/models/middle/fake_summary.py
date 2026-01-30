from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 刷单汇总表
class FakeSummaryManager(models.Manager):
    def add(self, shop_id, create_date, order_amount, order_num, fake_amount, fake_num, commission, freight, fake_note):
        return self.create(shop_id=shop_id, create_date=create_date, order_amount=order_amount, order_num=order_num, fake_amount=fake_amount, fake_num=fake_num, commission=commission, freight=freight, fake_note=fake_note)

    def set(self, pk, fake_amount, fake_num, commission, freight, fake_note):
        fake = self.get(pk=pk)
        fake.fake_amount = fake_amount
        fake.fake_num = fake_num
        fake.commission = commission
        fake.freight = freight
        fake.fake_note = fake_note
        return fake.save()
    
    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self):
        return self.all().count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id).order_by('-ctime')[left:right]

    def encoder(self, fake):
        return model_to_dict(fake, fields=['id', 'shop_id', 'create_date', 'order_num', 'fake_num', 'fake_amount', 'commission', 'freight', 'fake_note'])

    def encoderList(self, fakes):
        return [model_to_dict(fake, fields=['id', 'shop_id', 'create_date', 'order_num', 'fake_num', 'fake_amount', 'commission', 'freight', 'fake_note']) for fake in fakes]

class FakeSummary(models.Model):
    objects = FakeSummaryManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 刷单日期
    order_amount = models.DecimalField(max_digits=6, decimal_places=2) # 真实总金额
    order_num = models.IntegerField() # 真实订单数
    fake_amount = models.DecimalField(max_digits=6, decimal_places=2) # 刷单总金额
    fake_num = models.IntegerField() # 刷单订单数
    commission = models.DecimalField(max_digits=6, decimal_places=2) # 佣金
    freight = models.DecimalField(max_digits=6, decimal_places=2) # 运费
    fake_note = models.CharField(max_length=32) # 刷单备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_fake_summary'
