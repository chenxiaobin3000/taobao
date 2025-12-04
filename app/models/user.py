from django.db import models

class user(models.Model):
    user_name = models.CharField(max_length=20)

    class Meta(object):
        db_table = 't_user'
