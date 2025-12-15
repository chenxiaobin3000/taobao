from django.db import models
from django.utils import timezone

# 用户表
class User(models.Model):
    name = models.CharField(max_length = 16, db_index = True, unique = True)
    phone = models.CharField(max_length = 11, db_index = True)
    did = models.IntegerField(db_index = True) # 部门id
    rid = models.IntegerField(db_index = True) # 角色id
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_user'
