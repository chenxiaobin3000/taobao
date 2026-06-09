from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict


class ReceiptOwnerManager(models.Manager):
    def add(self, company, company_id):
        return self.create(company=company, company_id=company_id)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self):
        return self.count()

    def existsOwner(self, company, company_id):
        return self.filter(company=company, company_id=company_id).exists()

    def getList(self, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.order_by('-ctime')[left:right])

    def encoderList(self, owners):
        if owners:
            return [model_to_dict(owner, fields=['id', 'company', 'company_id']) for owner in owners]
        return None


class ReceiptOwner(models.Model):
    objects = ReceiptOwnerManager()
    company = models.CharField(max_length=20)
    company_id = models.CharField(max_length=20)
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_receipt_owner'
