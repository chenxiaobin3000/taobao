from django.db import models
from django.utils import timezone

# 权限表
class permission(models.Model):
    rid = models.IntegerField(db_index = True) # 角色id
    pid = models.IntegerField(db_index = True) # 权限
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_permission'
