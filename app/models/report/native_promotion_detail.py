from django.db import connection
from app.models.model import Model

# 推广表
class NativePromotionDetail(Model):
    def getSumByDateRange(self, shop_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT good_id,
                    COALESCE(SUM(cost), 0) AS cost,
	                COALESCE(SUM(deal_amount), 0) AS deal_amount,
	                COALESCE(SUM(deal_num), 0) AS deal_num,
                    COALESCE(SUM(shop_cart), 0) AS shop_cart,
                    COALESCE(SUM(favorites), 0) AS favorites
                FROM t_promotion_detail
                WHERE
	                shop_id = %s
	                AND promotion_date > %s
	                AND promotion_date < %s
                GROUP BY good_id""", [shop_id, start_date, end_date])
            return self.dictfetchall(cursor)

    def getSumByDateRangeIncludeStart(self, shop_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT good_id,
                    COALESCE(SUM(cost), 0) AS cost,
	                COALESCE(SUM(deal_amount), 0) AS deal_amount,
	                COALESCE(SUM(deal_num), 0) AS deal_num
                FROM t_promotion_detail
                WHERE
	                shop_id = %s
	                AND promotion_date >= %s
	                AND promotion_date < %s
                GROUP BY good_id""", [shop_id, start_date, end_date])
            return self.dictfetchall(cursor)
