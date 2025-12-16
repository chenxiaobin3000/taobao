from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 店铺表
class ShopManager(models.Manager):
    def add(self, company_id, name):
        return self.create(user_id=company_id, name=name)

    def set(self, pk, company_id, name):
        company = self.get(pk=pk)
        company.company_id = company_id
        company.name = name
        return company.save()

    def delete(self, pk):
        return self.filter(pk=pk).delete()

    def find(self, pk):
        return self.filter(pk=pk)

    def getList(self, user_id):
        return self.filter(user_id=user_id)
    
class Shop(models.Model):
    objects = ShopManager()
    company_id = models.IntegerField(db_index = True) # 归属公司id
    name = models.CharField(max_length = 16, db_index = True, unique = True) # 店铺名称
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_Sshop'
