from datetime import timedelta
from django.db import models
from django.utils import timezone

# 会话表
class SessionManager(models.Manager):
    def add(self, account, token):
        self.filter(token=token).exclude(account=account).delete()
        session, _ = self.update_or_create(
            account=account,
            defaults={
                'token': token,
                'ctime': timezone.now()
            }
        )
        return session

    # 删除指定天数之前的数据
    def delete(self, day):
        ago = timezone.now() - timedelta(days=day)
        return self.filter(ctime__lt=ago).delete()

    def getByToken(self, token):
        return self.filter(token=token).first()

    def deleteByToken(self, token):
        return self.filter(token=token).delete()

    def deleteByAccount(self, account):
        return self.filter(account=account).delete()

class Session(models.Model):
    objects = SessionManager()
    account = models.IntegerField(db_index = True, unique = True) # 账号id
    token = models.CharField(max_length = 32, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_session'
