from django.db import connection
from app.models.model import Model

# 商品表
class Good(Model):
    def getList(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM t_shop WHERE id=%s", [shop_id])
            return self.dictfetchall(cursor)
