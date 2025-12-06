from django.db import models

class order(models.Model):
    user_name = models.CharField(max_length=20)

    class Meta(object):
        db_table = 't_order'
