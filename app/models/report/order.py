from django.db import connection
from app.models.model import Model

# 订单表
class Order(Model):
    def total(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    count(t_order_summary.id) as total,
                    sum(t_order_summary.payment) as payment,
                    sum(t_order_summary.refund_customer) as refund_customer,
                    sum(t_order_summary.refund_platform) as refund_platform,
                    sum(t_order_summary.procure) as procure,
                    sum(t_order_summary.refund_procure) as refund_procure,
                    sum(t_order_summary.transfer) as transfer,
                    sum(t_order_summary.deduction) as deduction
                FROM t_order_summary
                WHERE t_order_summary.shop_id = %s""", [shop_id])
            return self.dictfetchall(cursor)[0]

    def totalByStatus(self, shop_id, status):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    count(t_order_summary.id) as total,
                    sum(t_order_summary.payment) as payment,
                    sum(t_order_summary.refund_customer) as refund_customer,
                    sum(t_order_summary.refund_platform) as refund_platform,
                    sum(t_order_summary.procure) as procure,
                    sum(t_order_summary.refund_procure) as refund_procure,
                    sum(t_order_summary.transfer) as transfer,
                    sum(t_order_summary.deduction) as deduction
                FROM t_order_summary
                WHERE t_order_summary.shop_id = %s
                and t_order_summary.order_status = %s""", [shop_id, status])
            return self.dictfetchall(cursor)[0]

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM t_order_summary
                WHERE t_order_summary.shop_id = %s
                ORDER BY t_order_summary.create_time DESC
                LIMIT %s
                OFFSET %s""", [shop_id, num, left])
            return self.dictfetchall(cursor)

    def getListByStatus(self, shop_id, status, page, num):
        left = (page - 1) * num
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM t_order_summary
                WHERE t_order_summary.shop_id = %s
                and t_order_summary.order_status = %s
                ORDER BY t_order_summary.create_time DESC
                LIMIT %s
                OFFSET %s""", [shop_id, status, num, left])
            return self.dictfetchall(cursor)
