from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 用户表
class UserManager(models.Manager):
    def add(self, name, phone, company_id, role_id):
        return self.create(name=name, phone=phone, company_id=company_id, role_id=role_id)

    def set(self, pk, name, phone, company_id, role_id):
        user = self.get(pk=pk)
        user.name = name
        user.phone = phone
        user.company_id = company_id
        user.role_id = role_id
        return user.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def getByPhone(self, phone):
        return self.filter(phone=phone).first()

    def getList(self, company_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(company_id=company_id)[left:right]

    def encoder(self, user):
        return model_to_dict(user, fields=['id', 'name', 'phone', 'company_id', 'role_id'])

    def encoderList(self, users):
        return [model_to_dict(user, fields=['id', 'name', 'phone', 'company_id', 'role_id']) for user in users]
    
class User(models.Model):
    objects = UserManager()
    name = models.CharField(max_length = 16, db_index = True, unique = True)
    phone = models.CharField(max_length = 11, db_index = True)
    company_id = models.IntegerField(db_index = True) # 公司id
    role_id = models.IntegerField(db_index = True) # 角色id
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_user'
