from django.db import connection
from app.models.model import Model

# 订单表
class NativeOrder(Model):
    def _append_filters(self, where, params, start_date=None, end_date=None, search=None, good_id_search=None):
        if start_date:
            where.append("create_time >= %s")
            params.append(start_date)
        if end_date:
            where.append("create_time < %s")
            params.append(end_date)
        if good_id_search:
            keyword = str(good_id_search).strip()
            if keyword:
                where.append("good_ids LIKE %s")
                params.append(f"%{keyword}%")
            return
        if search:
            keyword = str(search).strip()
            if keyword:
                where.append("order_id = %s")
                params.append(keyword)

    def total(self, shop_id, start_date=None, end_date=None, search=None, good_id_search=None):
        where = ["shop_id = %s"]
        params = [shop_id]
        self._append_filters(where, params, start_date, end_date, search, good_id_search)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    COUNT(id) as total,
                    COALESCE(SUM(payment), 0) as payment,
                    COALESCE(SUM(refund_customer), 0) as refund_customer,
                    COALESCE(SUM(refund_platform), 0) as refund_platform,
                    COALESCE(SUM(procure), 0) as procure,
                    COALESCE(SUM(refund_procure), 0) as refund_procure,
                    COALESCE(SUM(transfer), 0) as transfer,
                    COALESCE(SUM(deduction), 0) as deduction
                FROM t_order_summary
                WHERE
                    {' AND '.join(where)}""", params)
            return self.dictfetchall(cursor)[0]

    def totalByStatus(self, shop_id, status, start_date=None, end_date=None, search=None, good_id_search=None):
        where = ["shop_id = %s", "order_status = %s"]
        params = [shop_id, status]
        self._append_filters(where, params, start_date, end_date, search, good_id_search)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    COUNT(id) as total,
                    COALESCE(SUM(payment), 0) as payment,
                    COALESCE(SUM(refund_customer), 0) as refund_customer,
                    COALESCE(SUM(refund_platform), 0) as refund_platform,
                    COALESCE(SUM(procure), 0) as procure,
                    COALESCE(SUM(refund_procure), 0) as refund_procure,
                    COALESCE(SUM(transfer), 0) as transfer,
                    COALESCE(SUM(deduction), 0) as deduction
                FROM t_order_summary
                WHERE
                    {' AND '.join(where)}""", params)
            return self.dictfetchall(cursor)[0]

    def getList(self, shop_id, page, num, start_date=None, end_date=None, search=None, good_id_search=None):
        left = (page - 1) * num
        where = ["shop_id = %s"]
        params = [shop_id]
        self._append_filters(where, params, start_date, end_date, search, good_id_search)
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

    def getListByStatus(self, shop_id, status, page, num, start_date=None, end_date=None, search=None, good_id_search=None):
        left = (page - 1) * num
        where = ["shop_id = %s", "order_status = %s"]
        params = [shop_id, status]
        self._append_filters(where, params, start_date, end_date, search, good_id_search)
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
                    COALESCE(SUM(payment), 0) AS payment,
                    COALESCE(SUM(refund_customer), 0) AS refund_customer,
                    COALESCE(SUM(refund_platform), 0) AS refund_platform,
                    COALESCE(SUM(procure), 0) AS procure,
                    COALESCE(SUM(refund_procure), 0) AS refund_procure,
                    COALESCE(SUM(transfer), 0) AS transfer,
                    COALESCE(SUM(deduction), 0) AS deduction
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
                    order_status,
                    COALESCE(SUM(payment), 0) AS payment,
                    COALESCE(SUM(procure), 0) AS procure,
                    COALESCE(SUM(refund_procure), 0) AS refund_procure
                FROM t_day_summary
                WHERE
                    shop_id IN ({placeholders})
                    AND create_date >= %s
                    AND create_date <= %s
                GROUP BY shop_id, create_date, order_status
                ORDER BY create_date DESC
                """, params)
            return self.dictfetchall(cursor)

    def groupByMonth(self, shop_id, order_status):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    strftime('%%Y-%%m', create_date) AS create_month,
                    COALESCE(SUM(payment), 0) AS payment,
                    COALESCE(SUM(refund_customer), 0) AS refund_customer,
                    COALESCE(SUM(refund_platform), 0) AS refund_platform,
                    COALESCE(SUM(procure), 0) AS procure,
                    COALESCE(SUM(refund_procure), 0) AS refund_procure,
                    COALESCE(SUM(transfer), 0) AS transfer,
                    COALESCE(SUM(deduction), 0) AS deduction,
                    COALESCE(SUM(fake), 0) AS fake
                FROM t_day_summary
                WHERE
                    shop_id = %s
                    AND order_status = %s
                GROUP BY create_month
                ORDER BY create_month DESC
                """, [shop_id, order_status])
            return self.dictfetchall(cursor)
