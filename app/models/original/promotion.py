from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 推广表
class Promotion(models.Model):
    create_time = models.DateField(db_index=True) # 交易日期
    payment = models.DecimalField(max_digits=10, decimal_places=2) # 应付
    promotion_note = models.CharField(max_length=1024) # 备注
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_promotion'
