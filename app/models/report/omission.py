from django.db import connection
from app.models.model import Model

# 扣费表
class Omission(Model):
    def total(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(t_deduction_summary.id) as total,
                    SUM(t_deduction_summary.amount) as amount
                FROM t_deduction_summary
				LEFT JOIN t_order
				on t_deduction_summary.order_id = t_order.order_id
				LEFT JOIN t_fake
				on t_deduction_summary.order_id = t_fake.order_id
                WHERE
                    t_deduction_summary.shop_id = %s
					AND t_order.order_id IS NULL 
					AND t_fake.order_id IS NULL
                """, [shop_id])
            return self.dictfetchall(cursor)[0]

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    t_deduction_summary.order_id,
					t_deduction_summary.amount,
                    t_deduction_summary.deduction_detail,
                    t_deduction_summary.ctime,
					t_order.order_id AS oid,
					t_fake.order_id AS fid
                FROM t_deduction_summary
				LEFT JOIN t_order
				on t_deduction_summary.order_id = t_order.order_id
				LEFT JOIN t_fake
				on t_deduction_summary.order_id = t_fake.order_id
                WHERE
                    t_deduction_summary.shop_id = %s
					AND t_order.order_id IS NULL 
					AND t_fake.order_id IS NULL
                ORDER BY t_deduction_summary.ctime DESC
                LIMIT %s
                OFFSET %s""", [shop_id, num, left])
            return self.dictfetchall(cursor)
