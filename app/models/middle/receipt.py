from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 发票表
class ReceiptManager(models.Manager):
    def add(self, shop_id, create_date, user_id, receipt_id, receipt_name, receipt_note):
        return self.create(shop_id=shop_id, create_date=create_date, user_id=user_id, receipt_id=receipt_id, receipt_name=receipt_name, receipt_note=receipt_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-create_date')[left:right])

    def encoderList(self, miscs):
        if miscs:
            return [model_to_dict(misc, fields=['id', 'shop_id', 'create_date', 'user_id', 'receipt_id', 'receipt_name', 'receipt_note']) for misc in miscs]
        return None

class Receipt(models.Model):
    objects = ReceiptManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    create_date = models.DateField(db_index=True) # 创建日期
    user_id = models.IntegerField(db_index=True) # 申请人
    receipt_id = models.DecimalField(max_digits=20, decimal_places=2) # 税号
    receipt_name = models.CharField(max_length=20, db_index=True) # 抬头
    receipt_note = models.CharField(max_length=20) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_receipt'
