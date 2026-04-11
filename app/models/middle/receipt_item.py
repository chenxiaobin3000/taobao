from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 发票项目表
class ReceiptItemManager(models.Manager):
    def add(self, project_name, project_note):
        return self.create(project_name=project_name, project_note=project_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-ctime')[left:right])

    def encoderList(self, items):
        if items:
            return [model_to_dict(item, fields=['id', 'project_name', 'project_note']) for item in items]
        return None

class ReceiptItem(models.Model):
    objects = ReceiptItemManager()
    project_name = models.CharField(max_length=20) # 项目
    project_note = models.CharField(max_length=20) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_receipt_item'
