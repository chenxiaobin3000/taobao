from django.db import models
from django.utils import timezone

# 账号表
class account(models.Model):
    account = models.CharField(max_length = 16, db_index = True, unique = True)
    password = models.CharField(max_length = 32)
    uid = models.IntegerField() # 用户id
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_account'
