from django.db import connection
from app.models.model import Model

# 刷单表
class Fake(Model):
    def getList(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM t_shop WHERE id=%s", [shop_id])
            return self.dictfetchall(cursor)
