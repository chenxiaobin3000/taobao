from django.db import models
from django.utils import timezone

# 会话表
class session(models.Model):
    uid = models.IntegerField(db_index = True, unique = True) # 用户id
    token = models.CharField(max_length = 32, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_session'
