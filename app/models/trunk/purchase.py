from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 采购表
class PurchaseManager(models.Manager):
    def add(self, purchase_id, payment, freight, total, order_status, create_time, product_name, purchase_note):
        return self.create(purchase_id=purchase_id, payment=payment, freight=freight, total=total, order_status=order_status, create_time=create_time, product_name=product_name, purchase_note=purchase_note)

    def set(self, pk, order_status):
        purchase = self.get(pk=pk)
        purchase.order_status = order_status
        return purchase.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getById(self, purchase_id):
        return self.encoder(self.filter(purchase_id=purchase_id).first())

    def filterByDate(self, start_date=None, end_date=None, search=None):
        queryset = self.all()
        if start_date:
            queryset = queryset.filter(create_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(create_time__lt=end_date)
        if search:
            keyword = str(search).strip()
            if keyword:
                queryset = queryset.filter(purchase_id=keyword)
        return queryset

    def total(self, start_date=None, end_date=None, search=None):
        return self.filterByDate(start_date, end_date, search).count()

    def getList(self, page, num, start_date=None, end_date=None, search=None):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filterByDate(start_date, end_date, search).order_by('-create_time')[left:right])

    def encoder(self, purchase):
        if purchase:
            return model_to_dict(purchase, fields=['id', 'purchase_id', 'payment', 'freight', 'total', 'order_status', 'create_time', 'product_name', 'purchase_note'])
        return None

    def encoderList(self, purchases):
        if purchases:
            return [model_to_dict(purchase, fields=['id', 'purchase_id', 'payment', 'freight', 'total', 'order_status', 'create_time', 'product_name', 'purchase_note']) for purchase in purchases]
        return None
    
class Purchase(models.Model):
    objects = PurchaseManager()
    purchase_id = models.CharField(max_length=20, db_index=True) # 采购id
    payment = models.DecimalField(max_digits=6, decimal_places=2) # 付款金额
    freight = models.DecimalField(max_digits=6, decimal_places=2) # 运费
    total = models.DecimalField(max_digits=6, decimal_places=2) # 付款总计
    order_status = models.IntegerField(db_index=True) # 状态
    create_time = models.DateTimeField(db_index=True) # 创建时间
    product_name = models.CharField(max_length=32) # 商品名称
    purchase_note = models.CharField(max_length=32) # 采购备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_purchase'
