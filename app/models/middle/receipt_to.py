from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 发票表
class ReceiptToManager(models.Manager):
    def add(self, shop_id, create_date, user_id, receipt_id, receipt_name, project_id, project_num, receipt_note):
        return self.create(shop_id=shop_id, create_date=create_date, user_id=user_id, receipt_id=receipt_id, receipt_name=receipt_name, project_id=project_id, project_num=project_num, receipt_note=receipt_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-create_date')[left:right])

    def encoderList(self, receipts):
        if receipts:
            return [model_to_dict(receipt, fields=['id', 'shop_id', 'create_date', 'user_id', 'receipt_id', 'receipt_name', 'project_id', 'project_num', 'receipt_note']) for receipt in receipts]
        return None

class ReceiptTo(models.Model):
    objects = ReceiptToManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 创建日期
    user_id = models.IntegerField(db_index=True) # 填报人
    receipt_id = models.DecimalField(max_digits=20, decimal_places=2) # 税号
    receipt_name = models.CharField(max_length=20, db_index=True) # 抬头
    project_id = models.IntegerField(db_index=True) # 项目编号
    project_num = models.IntegerField(db_index=True) # 数量
    receipt_note = models.CharField(max_length=20) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_receipt_to'
