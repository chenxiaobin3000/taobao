from django.urls import path
from app.views.original import deduction, deduction_discard, fake, order, polymerize, polymerize_discard, promotion_detail, promotion, purchase, refund, transfer

url_original = [
    # 扣费
    path('api/deduction/addList', deduction.addList),
    path('api/deduction/del', deduction.delete),
    path('api/deduction/getList', deduction.getList),

    # 扣费-废弃
    path('api/deduction_discard/del', deduction_discard.delete),
    path('api/deduction_discard/delAll', deduction_discard.deleteAll),
    path('api/deduction_discard/getList', deduction_discard.getList),

    # 刷单
    path('api/fake/addList', fake.addList),
    path('api/fake/del', fake.delete),
    path('api/fake/getList', fake.getList),

    # 订单
    path('api/order/addList', order.addList),
    path('api/order/del', order.delete),
    path('api/order/getList', order.getList),

    # 聚合
    path('api/polymerize/addList', polymerize.addList),
    path('api/polymerize/del', polymerize.delete),
    path('api/polymerize/getList', polymerize.getList),

    # 聚合-废弃
    path('api/polymerize_discard/del', polymerize_discard.delete),
    path('api/polymerize_discard/delAll', polymerize_discard.deleteAll),
    path('api/polymerize_discard/getList', polymerize_discard.getList),

    # 推广明细
    path('api/promotion_detail/addList', promotion_detail.addList),
    path('api/promotion_detail/del', promotion_detail.delete),
    path('api/promotion_detail/getList', promotion_detail.getList),

    # 推广
    path('api/promotion/addList', promotion.addList),
    path('api/promotion/del', promotion.delete),
    path('api/promotion/getList', promotion.getList),

    # 采购
    path('api/purchase/addList', purchase.addList),
    path('api/purchase/del', purchase.delete),
    path('api/purchase/getList', purchase.getList),

    # 退货
    path('api/refund/addList', refund.addList),
    path('api/refund/del', refund.delete),
    path('api/refund/getList', refund.getList),

    # 小额打款
    path('api/transfer/addList', transfer.addList),
    path('api/transfer/del', transfer.delete),
    path('api/transfer/getList', transfer.getList),
]
