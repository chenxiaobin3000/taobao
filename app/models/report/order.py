from django.db import connection
from app.models.model import Model

# 订单表
class Order(Model):
    def total(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT count(t_order.id) as total, sum(t_order.payment) as payment,
                sum(t_order.procure) as procure, sum(t_deduction_summary.amount) as amount
                FROM t_order
                LEFT JOIN t_deduction_summary
                ON t_order.order_id = t_deduction_summary.order_id
                WHERE t_order.shop_id = %s""", [shop_id])
            return self.dictfetchall(cursor)[0]

    def totalByStatus(self, shop_id, status):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT count(t_order.id) as total, sum(t_order.payment) as payment,
                sum(t_order.procure) as procure, sum(t_deduction_summary.amount) as amount
                FROM t_order
                LEFT JOIN t_deduction_summary
                ON t_order.order_id = t_deduction_summary.order_id
                WHERE t_order.shop_id = %s
                and t_order.order_status = %s""", [shop_id, status])
            return self.dictfetchall(cursor)[0]

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT t_order.order_id, t_order.payment, t_order.procure,
                t_order.order_status, t_order.create_time, t_order.good_ids,
                t_deduction_summary.amount, t_deduction_summary.deduction_detail
                FROM t_order
                LEFT JOIN t_deduction_summary
                ON t_order.order_id = t_deduction_summary.order_id
                WHERE t_order.shop_id = %s
                ORDER BY t_order.create_time DESC
                LIMIT %s
                OFFSET %s""", [shop_id, num, left])
            return self.dictfetchall(cursor)

    def getListByStatus(self, shop_id, status, page, num):
        left = (page - 1) * num
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT t_order.order_id, t_order.payment, t_order.procure,
                t_order.order_status, t_order.create_time, t_order.good_ids,
                t_deduction_summary.amount, t_deduction_summary.deduction_detail
                FROM t_order
                LEFT JOIN t_deduction_summary
                ON t_order.order_id = t_deduction_summary.order_id
                WHERE t_order.shop_id = %s
                and t_order.order_status = %s
                ORDER BY t_order.create_time DESC
                LIMIT %s
                OFFSET %s""", [shop_id, status, num, left])
            return self.dictfetchall(cursor)
