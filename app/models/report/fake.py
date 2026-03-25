from django.db import connection
from app.models.model import Model

# 刷单表
class Fake(Model):
    def groupByMonth(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    strftime('%%Y-%%m', create_date) AS create_month,
                    SUM(commission) AS commission,
					SUM(freight) AS freight
                FROM t_fake_summary
                WHERE
                    shop_id = %s
                GROUP BY create_month
                ORDER BY create_month DESC
                """, [shop_id])
            return self.dictfetchall(cursor)
