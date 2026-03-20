from django.db import connection
from app.models.model import Model

# 订单表
class Order(Model):
    def total(self, shop_id):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(id) as total,
                    SUM(payment) as payment,
                    SUM(refund_customer) as refund_customer,
                    SUM(refund_platform) as refund_platform,
                    SUM(procure) as procure,
                    SUM(refund_procure) as refund_procure,
                    SUM(transfer) as transfer,
                    SUM(deduction) as deduction
                FROM t_order_summary
                WHERE
                    shop_id = %s""", [shop_id])
            return self.dictfetchall(cursor)[0]

    def totalByStatus(self, shop_id, status):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(id) as total,
                    SUM(payment) as payment,
                    SUM(refund_customer) as refund_customer,
                    SUM(refund_platform) as refund_platform,
                    SUM(procure) as procure,
                    SUM(refund_procure) as refund_procure,
                    SUM(transfer) as transfer,
                    SUM(deduction) as deduction
                FROM t_order_summary
                WHERE
                    shop_id = %s
                    and order_status = %s""", [shop_id, status])
            return self.dictfetchall(cursor)[0]

    def getList(self, shop_id, page, num):
        left = (page - 1) * num
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT *
                FROM t_order_summary
                WHERE
                    shop_id = %s
                ORDER BY create_time DESC
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
                WHERE
                    shop_id = %s
                    AND order_status = %s
                ORDER BY create_time DESC
                LIMIT %s
                OFFSET %s""", [shop_id, status, num, left])
            return self.dictfetchall(cursor)

    def groupByDate(self, shop_id, order_status, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    strftime('%%Y-%%m-%%d', create_time) AS create_date,
                    SUM(payment) AS payment,
                    SUM(refund_customer) AS refund_customer,
                    SUM(refund_platform) AS refund_platform,
                    SUM(procure) AS procure,
                    SUM(refund_procure) AS refund_procure,
                    SUM(transfer) AS transfer,
                    SUM(deduction) AS deduction
                FROM t_order_summary
                WHERE
                    shop_id = %s
                    AND order_status = %s
                    AND create_time > %s
                    AND create_time < %s
                GROUP BY create_date
                ORDER BY create_date DESC
                """, [shop_id, order_status, start_date, end_date])
            return self.dictfetchall(cursor)

    def groupByMonth(self, shop_id, order_status):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    strftime('%%Y-%%m', create_time) AS create_month,
                    SUM(payment) AS payment,
                    SUM(refund_customer) AS refund_customer,
                    SUM(refund_platform) AS refund_platform,
                    SUM(procure) AS procure,
                    SUM(refund_procure) AS refund_procure,
                    SUM(transfer) AS transfer,
                    SUM(deduction) AS deduction
                FROM t_order_summary
                WHERE
                    shop_id = %s
                    AND order_status = %s
                GROUP BY create_month
                ORDER BY create_month DESC
                """, [shop_id, order_status])
            return self.dictfetchall(cursor)
