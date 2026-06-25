from django.db import connection
from app.models.model import Model

# 推广表
class NativePromotion(Model):
    def groupByMonth(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    strftime('%%Y-%%m', create_date) AS create_month,
                    COALESCE(SUM(payment), 0) AS payment
                FROM t_promotion
                WHERE
                    shop_id = %s
                GROUP BY create_month
                ORDER BY create_month DESC
                """, [shop_id])
            return self.dictfetchall(cursor)

    def groupByDateRange(self, shop_ids, start_date, end_date):
        if not shop_ids:
            return []
        placeholders = ','.join(['%s'] * len(shop_ids))
        params = list(shop_ids) + [start_date, end_date]
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    shop_id,
                    strftime('%%Y-%%m-%%d', create_date) AS create_date,
                    COALESCE(SUM(payment), 0) AS payment
                FROM t_promotion
                WHERE
                    shop_id IN ({placeholders})
                    AND create_date >= %s
                    AND create_date <= %s
                GROUP BY shop_id, create_date
                ORDER BY create_date DESC
                """, params)
            return self.dictfetchall(cursor)
