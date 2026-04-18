from django.db import connection
from app.models.model import Model

# 推广表
class NativePromotionDetail(Model):
    def getSumByDateRange(self, shop_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT good_id,
                    SUM(cost) AS cost,
	                SUM(deal_amount) AS deal_amount,
	                SUM(deal_num) AS deal_num
                FROM t_promotion_detail
                WHERE
	                shop_id = %s
	                AND promotion_date > %s
	                AND promotion_date < %s
                GROUP BY good_id""", [shop_id, start_date, end_date])
            return self.dictfetchall(cursor)
        
    def getListByDateRange(self, shop_id, start_date, end_date):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT good_id, promotion_date,
                    SUM(cost) AS cost,
	                SUM(deal_amount) AS deal_amount,
	                SUM(deal_num) AS deal_num
                FROM t_promotion_detail
                WHERE
	                shop_id = %s
	                AND promotion_date > %s
	                AND promotion_date < %s
                GROUP BY good_id, promotion_date
                ORDER BY promotion_date ASC""", [shop_id, start_date, end_date])
            return self.dictfetchall(cursor)
