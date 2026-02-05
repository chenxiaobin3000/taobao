from django.urls import path
from app.views.middle import deduction_summary, fake_summary, miscellaneous

url_middle = [
    # 扣款
    path('api/deduction_summary/flush', deduction_summary.flush),
    path('api/deduction_summary/getList', deduction_summary.getList),

    # 刷单
    path('api/fake_summary/flush', fake_summary.flush),
    path('api/fake_summary/set', fake_summary.set),
    path('api/fake_summary/getList', fake_summary.getList),

    # 杂项
    path('api/misc/add', miscellaneous.add),
    path('api/misc/set', miscellaneous.set),
    path('api/misc/del', miscellaneous.delete),
    path('api/misc/getList', miscellaneous.getList),
]
