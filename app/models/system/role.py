from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 角色表
class RoleManager(models.Manager):
    def add(self, company_id, name):
        return self.create(company_id=company_id, name=name)

    def set(self, pk, name):
        role = self.get(pk=pk)
        role.name = name
        return role.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.encoder(self.get(pk=pk))

    def total(self, company_id):
        return self.filter(company_id=company_id).count()

    def getList(self, company_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(company_id=company_id)[left:right])

    def encoder(self, role):
        if role:
            return model_to_dict(role, fields=['id', 'company_id', 'name'])
        return None

    def encoderList(self, roles):
        if roles:
            return [model_to_dict(role, fields=['id', 'company_id', 'name']) for role in roles]
        return None
    
class Role(models.Model):
    objects = RoleManager()
    company_id = models.IntegerField(db_index = True) # 归属公司id
    name = models.CharField(max_length = 16, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_role'
