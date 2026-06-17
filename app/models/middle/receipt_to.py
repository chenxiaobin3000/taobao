from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 发票表
class ReceiptToManager(models.Manager):
    def add(self, owner, create_date, user_id, project_id, project_num, receipt_id, receipt_note, amount, tax, tax_rate, company, company_id=''):
        return self.create(owner=owner, create_date=create_date, user_id=user_id, project_id=project_id, project_num=project_num, receipt_id=receipt_id, receipt_note=receipt_note, amount=amount, tax=tax, tax_rate=tax_rate, company=company, company_id=company_id)

    def existsReceipt(self, receipt_id):
        return self.filter(receipt_id=receipt_id).exists()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, owner):
        return self.filter(owner=owner).count()

    def getList(self, owner, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(owner=owner).order_by('-create_date')[left:right])

    def encoderList(self, receipts):
        if receipts:
            return [model_to_dict(receipt, fields=['id', 'owner', 'create_date', 'user_id', 'project_id', 'project_num', 'amount', 'tax', 'tax_rate', 'company', 'company_id', 'receipt_id', 'receipt_note']) for receipt in receipts]
        return None

class ReceiptTo(models.Model):
    objects = ReceiptToManager()
    owner = models.IntegerField(db_index=True) # 开票方
    create_date = models.DateField(db_index=True) # 创建日期
    user_id = models.IntegerField(db_index=True) # 填报人
    project_id = models.IntegerField(db_index=True) # 项目编号
    project_num = models.IntegerField(db_index=True) # 数量
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    tax = models.DecimalField(max_digits=10, decimal_places=2) # 税额
    tax_rate = models.IntegerField() # 税率
    company = models.CharField(max_length=20) # 抬头
    company_id = models.CharField(max_length=20, default='') # 税号
    receipt_id = models.CharField(max_length=20, db_index=True) # 发票号码
    receipt_note = models.CharField(max_length=20) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_receipt_to'
