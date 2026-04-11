from django.urls import path
from app.views.middle import deduction_summary, fake_summary, miscellaneous, order_summary, receipt_from, receipt_item, receipt_to

url_middle = [
    # 扣款
    path('api/deduction_summary/flush', deduction_summary.flush),
    path('api/deduction_summary/getList', deduction_summary.getList),

    # 刷单
    path('api/fake_summary/flush', fake_summary.flush),
    path('api/fake_summary/set', fake_summary.set),
        path('api/fake_summary/batch', fake_summary.batch),
    path('api/fake_summary/getList', fake_summary.getList),

    # 杂项
    path('api/misc/add', miscellaneous.add),
    path('api/misc/set', miscellaneous.set),
    path('api/misc/del', miscellaneous.delete),
    path('api/misc/getList', miscellaneous.getList),

    # 扣款
    path('api/order_summary/flush', order_summary.flush),
    path('api/order_summary/getList', order_summary.getList),

    # 进项票
    path('api/receipt_from/add', receipt_from.add),
    path('api/receipt_from/del', receipt_from.delete),
    path('api/receipt_from/getList', receipt_from.getList),

    # 发票项
    path('api/receipt_item/add', receipt_item.add),
    path('api/receipt_item/del', receipt_item.delete),
    path('api/receipt_item/getList', receipt_item.getList),

    # 发票
    path('api/receipt_to/add', receipt_to.add),
    path('api/receipt_to/del', receipt_to.delete),
    path('api/receipt_to/getList', receipt_to.getList),
]
