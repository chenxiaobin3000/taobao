from django.db import connection
from app.models.model import Model

# 推广表
class Promotion(Model):
    def groupByMonth(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    strftime('%%Y-%%m', create_date) AS create_month,
                    SUM(payment) AS payment
                FROM t_promotion
                WHERE
                    shop_id = %s
                GROUP BY create_month
                ORDER BY create_month DESC
                """, [shop_id])
            return self.dictfetchall(cursor)
