from django.db import models
from django.utils import timezone

# 平台表
class Market(models.Model):
    name = models.CharField(max_length = 8, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_market'
