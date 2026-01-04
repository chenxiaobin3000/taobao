from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 刷单表
class FakeManager(models.Manager):
    def add(self, name, user_id):
        return self.create(name=name, user_id=user_id)

    def set(self, pk, name, user_id):
        company = self.get(pk=pk)
        company.name = name
        company.user_id = user_id
        return company.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getList(self, page, num):
        left = (page - 1) * num
        right = page * num
        return self.all()[left:right]

    def encoder(self, company):
        return model_to_dict(company, fields=['id', 'name', 'user_id'])

    def encoderList(self, companys):
        return [model_to_dict(company, fields=['id', 'name', 'user_id']) for company in companys]
    
class Fake(models.Model):
    objects = FakeManager()
    create_date = models.DateField(db_index=True) # 刷单日期
    real_num = models.IntegerField() # 真实订单数
    fake_amount = models.IntegerField() # 刷单总金额
    fake_num = models.IntegerField() # 刷单订单数
    commission = models.DecimalField(max_digits=6, decimal_places=2) # 实际付款
    freight = models.DecimalField(max_digits=6, decimal_places=2) # 运费
    fake_note = models.CharField(max_length=32) # 刷单备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_fake'
