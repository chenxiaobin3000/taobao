from django.db import connection
from app.models.model import Model

# 扣费表
class Omission(Model):
    def total(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT count(id) as total, sum(amount) as amount
                FROM t_deduction_summary
                WHERE t_deduction_summary.shop_id = %s
                and NOT EXISTS (
                    SELECT id
                    FROM t_order
                    WHERE t_order.shop_id = %s 
                    and t_deduction_summary.order_id = t_order.order_id
                )""", [shop_id, shop_id])
            return self.dictfetchall(cursor)[0]

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM t_deduction_summary
                WHERE t_deduction_summary.shop_id = %s
                and NOT EXISTS (
                    SELECT id
                    FROM t_order
                    WHERE t_order.shop_id = %s 
                    and t_deduction_summary.order_id = t_order.order_id
                )
                ORDER BY t_deduction_summary.ctime DESC
                LIMIT %s
                OFFSET %s""", [shop_id, shop_id, num, left])
            return self.dictfetchall(cursor)
