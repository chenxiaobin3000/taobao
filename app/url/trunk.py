from django.urls import path
from app.views.trunk import deduction, fake, order, polymerize, promotion_detail, promotion, purchase, refund, transfer

url_trunk = [
    # 扣费
    path('api/deduction/addList', deduction.addList),
    path('api/deduction/del', deduction.delete),
    path('api/deduction/getList', deduction.getList),

    # 刷单
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
