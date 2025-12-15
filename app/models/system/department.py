from django.db import models
from django.utils import timezone

# 部门表
class Department(models.Model):
    name = models.CharField(max_length = 16, db_index = True, unique = True)
    parent = models.IntegerField() # 上级部门id
    level = models.IntegerField() # 层级
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_department'
