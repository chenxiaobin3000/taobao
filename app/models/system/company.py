from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict
from app.models.const.company_status import CompanyStatus

# 公司表
class CompanyManager(models.Manager):
    def add(self, name, user_id):
        return self.create(name=name, user_id=user_id, company_status=CompanyStatus.NORMAL)

    def set(self, pk, name, user_id):
        company = self.get(pk=pk)
        company.name = name
        company.user_id = user_id
        return company.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self):
        return self.all().count()

    def getList(self, page, num):
        left = (page - 1) * num
        right = page * num
        return self.all()[left:right]

    def encoder(self, company):
        return model_to_dict(company, fields=['id', 'name', 'user_id', 'company_status'])

    def encoderList(self, companys):
        return [model_to_dict(company, fields=['id', 'name', 'user_id', 'company_status']) for company in companys]
    
class Company(models.Model):
    objects = CompanyManager()
    name = models.CharField(max_length = 16, db_index = True, unique = True) # 公司名称
    user_id = models.IntegerField(db_index=True) # 负责人id
    company_status = models.IntegerField(db_index=True) # 公司状态
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_company'
