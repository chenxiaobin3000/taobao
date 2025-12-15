from django.db import models
from django.utils import timezone

# 账号表
class AccountManager(models.Manager):
    def add(self, account, password):
        return self.create(account=account, password=password, user_id=0)

    def set(self, pk, account, password, user_id):
        return self.filter(pk=pk).update(account=account, password=password, user_id=user_id)

    def delete(self, pk):
        return self.filter(pk=pk).delete()

    def get(self, pk):
        return self.filter(pk=pk)

    def getList(self, user_id):
        return self.filter(user_id=user_id)

class Account(models.Model):
    account = models.CharField(max_length=16, db_index=True, unique=True)
    password = models.CharField(max_length=32)
    user_id = models.IntegerField(db_index=True) # 用户id
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_account'
