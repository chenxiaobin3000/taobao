from django.urls import path
from app.views.middle import deduction_summary, fake_summary, miscellaneous

url_middle = [
    # 扣款
    path('api/middle/deduction_summary/flush', deduction_summary.flush),
    path('api/middle/deduction_summary/getList', deduction_summary.getList),

    # 刷单
    path('api/middle/fake_summary/flush', fake_summary.flush),
    path('api/middle/fake_summary/set', fake_summary.set),
    path('api/middle/fake_summary/getList', fake_summary.getList),

    # 杂项
    path('api/middle/misc/add', miscellaneous.add),
    path('api/middle/misc/set', miscellaneous.set),
    path('api/middle/misc/del', miscellaneous.delete),
    path('api/middle/misc/getList', miscellaneous.getList),
]
