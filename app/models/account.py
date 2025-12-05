from django.db import models

class baseOrder(models.Model):
    account_name = models.CharField(max_length=20)
    account_pwd = models.CharField(max_length=32)

    class Meta(object):
        db_table = 't_account'
