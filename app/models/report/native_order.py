from django.db import connection
from app.models.model import Model

# 订单表
class NativeOrder(Model):
    def _append_filters(self, where, params, start_date=None, end_date=None, search=None):
        if start_date:
            where.append("create_time >= %s")
            params.append(start_date)
        if end_date:
            where.append("create_time < %s")
            params.append(end_date)
        if search:
            keyword = str(search).strip()
            if keyword:
                where.append("order_id = %s")
                params.append(keyword)

    def total(self, shop_id, start_date=None, end_date=None, search=None):
        where = ["shop_id = %s"]
        params = [shop_id]
        self._append_filters(where, params, start_date, end_date, search)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
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
                    {' AND '.join(where)}""", params)
            return self.dictfetchall(cursor)[0]

    def totalByStatus(self, shop_id, status, start_date=None, end_date=None, search=None):
        where = ["shop_id = %s", "order_status = %s"]
        params = [shop_id, status]
        self._append_filters(where, params, start_date, end_date, search)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
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
                    {' AND '.join(where)}""", params)
            return self.dictfetchall(cursor)[0]

    def getList(self, shop_id, page, num, start_date=None, end_date=None, search=None):
        left = (page - 1) * num
        where = ["shop_id = %s"]
        params = [shop_id]
        self._append_filters(where, params, start_date, end_date, search)
        params.extend([num, left])
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT *
                FROM t_order_summary
                WHERE
                    {' AND '.join(where)}
                ORDER BY create_time DESC
                LIMIT %s
                OFFSET %s""", params)
            return self.dictfetchall(cursor)

    def getListByStatus(self, shop_id, status, page, num, start_date=None, end_date=None, search=None):
        left = (page - 1) * num
        where = ["shop_id = %s", "order_status = %s"]
        params = [shop_id, status]
        self._append_filters(where, params, start_date, end_date, search)
        params.extend([num, left])
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT *
                FROM t_order_summary
                WHERE
                    {' AND '.join(where)}
                ORDER BY create_time DESC
                LIMIT %s
                OFFSET %s""", params)
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
                    strftime('%%Y-%%m', create_date) AS create_month,
                    SUM(payment) AS payment,
                    SUM(refund_customer) AS refund_customer,
                    SUM(refund_platform) AS refund_platform,
                    SUM(procure) AS procure,
                    SUM(refund_procure) AS refund_procure,
                    SUM(transfer) AS transfer,
                    SUM(deduction) AS deduction,
                    SUM(fake) AS fake
                FROM t_day_summary
                WHERE
                    shop_id = %s
                    AND order_status = %s
                GROUP BY create_month
                ORDER BY create_month DESC
                """, [shop_id, order_status])
            return self.dictfetchall(cursor)
