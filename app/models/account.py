from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 账号表
class AccountManager(models.Manager):
    def add(self, account, password, user_id):
        return self.create(account=account, password=password, user_id=user_id)

    def set(self, pk, password):
        account = self.get(pk=pk)
        account.password = password
        return account.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def getByAccount(self, account):
        return self.encoder(self.filter(account=account).first())

    def total(self):
        return self.all().count()

    def getList(self, user_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoder(self.filter(user_id=user_id)[left:right])

    def encoder(self, account):
        if account:
            return model_to_dict(account, fields=['id', 'account', 'password', 'user_id'])
        return None

    def encoderList(self, accounts):
        if accounts:
            return [model_to_dict(account, fields=['id', 'account', 'password', 'user_id']) for account in accounts]
        return None

class Account(models.Model):
    objects = AccountManager()
    account = models.CharField(max_length=16, db_index=True, unique=True) # 账号
    password = models.CharField(max_length=32) # 密码
    user_id = models.IntegerField(db_index=True) # 用户id
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_account'
