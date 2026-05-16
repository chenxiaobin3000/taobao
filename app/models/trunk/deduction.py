from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 扣费表
class DeductionManager(models.Manager):
    def add(self, shop_id, order_id, finance_type, amount, amount_type, create_time, deduction_note):
        return self.create(shop_id=shop_id, order_id=order_id, finance_type=finance_type, amount=amount, amount_type=amount_type, create_time=create_time, deduction_note=deduction_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByCTime(self, shop_id, order_id, amount_type, create_time):
        return self.encoder(self.filter(shop_id=shop_id, order_id=order_id, amount_type=amount_type, create_time=create_time).first())

    def filterByDate(self, shop_id, start_date=None, end_date=None, search=None):
        queryset = self.filter(shop_id=shop_id)
        if start_date:
            queryset = queryset.filter(create_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(create_time__lt=end_date)
        if search:
            keyword = str(search).strip()
            if keyword:
                queryset = queryset.filter(order_id=keyword)
        return queryset

    def total(self, shop_id, start_date=None, end_date=None, search=None):
        return self.filterByDate(shop_id, start_date, end_date, search).count()

    def getList(self, shop_id, page, num, start_date=None, end_date=None, search=None):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filterByDate(shop_id, start_date, end_date, search).order_by('-create_time')[left:right])

    def getAll(self, shop_id, start_date):
        return self.encoderList(self.filter(shop_id=shop_id, create_time__gt=start_date))

    def encoder(self, deduction):
        if deduction:
            return model_to_dict(deduction, fields=['id', 'order_id', 'finance_type', 'amount', 'amount_type', 'create_time', 'deduction_note'])
        return None

    def encoderList(self, deductions):
        if deductions:
            return [model_to_dict(deduction, fields=['id', 'order_id', 'finance_type', 'amount', 'amount_type', 'create_time', 'deduction_note']) for deduction in deductions]
        return None
    
class Deduction(models.Model):
    objects = DeductionManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    finance_type = models.IntegerField(db_index=True) # 财务类型
    amount = models.DecimalField(max_digits=10, decimal_places=2) # 金额
    amount_type = models.IntegerField(db_index=True) # 扣费类型
    create_time = models.DateTimeField(db_index=True) # 创建时间
    deduction_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_deduction'
