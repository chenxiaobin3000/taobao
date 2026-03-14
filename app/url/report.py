from django.urls import path
from app.views.report import cost_report, day_report, fake_report, good_radar, good_report, order_report, omission_report, year_report

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
    path('api/good_report/getList', good_report.getList),

    # 订单报表
    path('api/order_report/getList', order_report.getList),

    # 遗漏报表
    path('api/omission_report/getList', omission_report.getList),

    # 年报
    path('api/year_report/getList', year_report.getList),
]
