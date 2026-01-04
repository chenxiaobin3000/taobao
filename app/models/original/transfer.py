from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 小额打款表
class TransferManager(models.Manager):
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
    
class Transfer(models.Model):
    objects = TransferManager()
    user_id = models.IntegerField(db_index=True) # 打款人
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=6, decimal_places=2) # 金额
    create_time = models.DateTimeField(db_index=True) # 创建时间
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_transfer'
