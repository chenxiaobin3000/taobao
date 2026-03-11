from django.urls import path
from app.views.trunk import deduction, fake, order, polymerize, promotion_detail, promotion, purchase, refund, transfer

url_trunk = [
    # 扣费
    path('api/deduction/merge', deduction.merge),
    path('api/deduction/del', deduction.delete),
    path('api/deduction/getList', deduction.getList),

    # 刷单
    path('api/fake/merge', fake.merge),
    path('api/fake/del', fake.delete),
    path('api/fake/getList', fake.getList),

    # 订单
    path('api/order/merge', order.merge),
    path('api/order/del', order.delete),
    path('api/order/getList', order.getList),

    # 聚合
    path('api/polymerize/merge', polymerize.merge),
    path('api/polymerize/del', polymerize.delete),
    path('api/polymerize/getList', polymerize.getList),

    # 推广明细
    path('api/promotion_detail/merge', promotion_detail.merge),
    path('api/promotion_detail/del', promotion_detail.delete),
    path('api/promotion_detail/getList', promotion_detail.getList),

    # 推广
    path('api/promotion/merge', promotion.merge),
    path('api/promotion/del', promotion.delete),
    path('api/promotion/getList', promotion.getList),

    # 采购
    path('api/purchase/merge', purchase.merge),
    path('api/purchase/del', purchase.delete),
    path('api/purchase/getList', purchase.getList),

    # 退货
    path('api/refund/merge', refund.merge),
    path('api/refund/del', refund.delete),
    path('api/refund/getList', refund.getList),

    # 小额打款
    path('api/transfer/merge', transfer.merge),
    path('api/transfer/del', transfer.delete),
    path('api/transfer/getList', transfer.getList),
]
