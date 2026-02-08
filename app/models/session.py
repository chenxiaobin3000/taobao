from datetime import timedelta
from django.db import models
from django.utils import timezone

# 会话表
class SessionManager(models.Manager):
    def add(self, account, token):
        return self.create(account=account, token=token)

    # 删除指定天数之前的数据
    def delete(self, day):
        ago = timezone.now() - timedelta(days=day)
        return self.filter(ctime__lt=ago).delete()

    def check(self, token):
        return self.filter(token=token).first()

class Session(models.Model):
    objects = SessionManager()
    account = models.IntegerField(db_index = True, unique = True) # 账号id
    token = models.CharField(max_length = 32, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_session'
