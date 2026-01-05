from django.urls import path
from app.views.original import deduction, miscellaneous, order, polymerize, promotion_detail, promotion, purchase, refund, transfer

url_original = [
    # 扣费
    path('api/deduction/add', deduction.add),
    path('api/deduction/del', deduction.delete),
    path('api/deduction/get', deduction.get),
    path('api/deduction/getList', deduction.getList),

    # 杂项
    path('api/misc/add', miscellaneous.add),
    path('api/misc/set', miscellaneous.set),
    path('api/misc/del', miscellaneous.delete),
    path('api/misc/get', miscellaneous.get),
    path('api/misc/getList', miscellaneous.getList),

    # 订单
    path('api/order/add', order.add),
    path('api/order/set', order.set),
    path('api/order/del', order.delete),
    path('api/order/get', order.get),
    path('api/order/getList', order.getList),

    # 聚合
    path('api/polymerize/add', polymerize.add),
    path('api/polymerize/del', polymerize.delete),
    path('api/polymerize/get', polymerize.get),
    path('api/polymerize/getList', polymerize.getList),

    # 推广明细
    path('api/promotion_detail/add', promotion_detail.add),
    path('api/promotion_detail/del', promotion_detail.delete),
    path('api/promotion_detail/get', promotion_detail.get),
    path('api/promotion_detail/getList', promotion_detail.getList),

    # 推广
    path('api/promotion/add', promotion.add),
    path('api/promotion/del', promotion.delete),
    path('api/promotion/get', promotion.get),
    path('api/promotion/getList', promotion.getList),

    # 采购
    path('api/purchase/add', purchase.add),
    path('api/purchase/set', purchase.set),
    path('api/purchase/del', purchase.delete),
    path('api/purchase/get', purchase.get),
    path('api/purchase/getList', purchase.getList),

    # 退货
    path('api/refund/add', refund.add),
    path('api/refund/set', refund.set),
    path('api/refund/del', refund.delete),
    path('api/refund/get', refund.get),
    path('api/refund/getList', refund.getList),

    # 小额打款
    path('api/transfer/add', transfer.add),
    path('api/transfer/del', transfer.delete),
    path('api/transfer/get', transfer.get),
    path('api/transfer/getList', transfer.getList),
]
