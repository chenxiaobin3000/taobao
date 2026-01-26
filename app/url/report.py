from django.urls import path
from app.views.report import cost_report, day_report, fake_report, good_radar, good_report, order_report, year_report

url_report = [
    # 成本报表
    path('api/cost_report/getList', cost_report.getList),

    # 日报
    path('api/day_report/getList', day_report.getList),

    # 刷单报表
    path('api/fake_report/getList', fake_report.getList),

    # 商品雷达
    path('api/good_radar/getList', good_radar.getList),

    # 商品报表
    path('api/good_report/get', good_report.get),

    # 订单报表
    path('api/order_report/flush', order_report.flush),

    # 年报
    path('api/year_report/get', year_report.get),
]
