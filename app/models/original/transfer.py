from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 小额打款表
class TransferManager(models.Manager):
    def add(self, shop_id, user_name, payee_name, order_id, amount, create_time, transfer_note):
        return self.create(shop_id=shop_id, user_name=user_name, payee_name=payee_name, order_id=order_id, amount=amount, create_time=create_time, transfer_note=transfer_note)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByCTime(self, shop_id, create_time):
        return self.encoder(self.filter(shop_id=shop_id, create_time=create_time).first())

    def total(self, shop_id):
        return self.filter(shop_id=shop_id).count()

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(shop_id=shop_id).order_by('-create_time')[left:right])

    def encoder(self, transfer):
        if transfer:
            return model_to_dict(transfer, fields=['id', 'shop_id', 'user_name', 'payee_name', 'order_id', 'amount', 'create_time', 'transfer_note'])
        return None

    def encoderList(self, transfers):
        if transfers:
            return [model_to_dict(transfer, fields=['id', 'shop_id', 'user_name', 'payee_name', 'order_id', 'amount', 'create_time', 'transfer_note']) for transfer in transfers]
        return None
    
class Transfer(models.Model):
    objects = TransferManager()
    shop_id = models.IntegerField(db_index = True) # 店铺id
    user_name = models.CharField(max_length=20, db_index=True) # 打款人
    payee_name = models.CharField(max_length=20, db_index=True) # 受款人
    order_id = models.CharField(max_length=20, db_index=True) # 订单id
    amount = models.DecimalField(max_digits=6, decimal_places=2) # 金额
    create_time = models.DateTimeField(db_index=True) # 创建时间
    transfer_note = models.CharField(max_length=64) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_transfer'
