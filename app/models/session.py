from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 会话表
class SessionManager(models.Manager):
    def add(self, account, token):
        return self.create(account=account, token=token)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def encoder(self, session):
        return model_to_dict(session, fields=['id', 'account', 'token'])

class Session(models.Model):
    objects = SessionManager()
    account = models.IntegerField(db_index = True, unique = True) # 账号id
    token = models.CharField(max_length = 32, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_session'
