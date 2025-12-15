from django.db import models
from django.utils import timezone

# 角色表
class Role(models.Model):
    name = models.CharField(max_length = 16, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_role'
