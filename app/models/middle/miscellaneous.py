from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 杂项表
class MiscellaneousManager(models.Manager):
    def add(self, shop_id, create_date, user_id, project_name, amount, misc_note):
        return self.create(shop_id=shop_id, create_date=create_date, user_id=user_id, project_name=project_name, amount=amount, misc_note=misc_note)

    def set(self, pk, project_name, amount, misc_note):
        misc = self.get(pk=pk)
        misc.project_name = project_name
        misc.amount = amount
        misc.misc_note = misc_note
        return misc.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self):
        return self.all().count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.filter(shop_id=shop_id)[left:right]

    def encoder(self, misc):
        return model_to_dict(misc, fields=['id', 'create_date', 'user_id', 'project_name', 'amount', 'misc_note'])

    def encoderList(self, miscs):
        return [model_to_dict(misc, fields=['id', 'create_date', 'user_id', 'project_name', 'amount', 'misc_note']) for misc in miscs]
    
class Miscellaneous(models.Model):
    objects = MiscellaneousManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 创建日期
    user_id = models.IntegerField(db_index=True) # 打款人
    project_name = models.CharField(max_length=32, db_index=True) # 项目名称
    amount = models.DecimalField(max_digits=6, decimal_places=2) # 金额
    misc_note = models.CharField(max_length=32) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_miscellaneous'
