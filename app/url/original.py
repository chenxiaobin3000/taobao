from django.urls import path
from app.views.original import user_deduction, user_deduction_discard, user_fake, user_order, user_polymerize, user_polymerize_discard, user_promotion_detail, user_promotion, user_purchase, user_refund, user_transfer

url_original = [
    # 扣费
    path('api/user_deduction/addList', user_deduction.addList),
    path('api/user_deduction/del', user_deduction.delete),
    path('api/user_deduction/getList', user_deduction.getList),

    # 扣费-废弃
    path('api/user_deduction_discard/del', user_deduction_discard.delete),
    path('api/user_deduction_discard/delAll', user_deduction_discard.deleteAll),
    path('api/user_deduction_discard/getList', user_deduction_discard.getList),

    # 刷单
    path('api/user_fake/addList', user_fake.addList),
    path('api/user_fake/del', user_fake.delete),
    path('api/user_fake/getList', user_fake.getList),

    # 订单
    path('api/user_order/addList', user_order.addList),
    path('api/user_order/del', user_order.delete),
    path('api/user_order/getList', user_order.getList),

    # 聚合
    path('api/user_polymerize/addList', user_polymerize.addList),
    path('api/user_polymerize/del', user_polymerize.delete),
    path('api/user_polymerize/getList', user_polymerize.getList),

    # 聚合-废弃
    path('api/user_polymerize_discard/del', user_polymerize_discard.delete),
    path('api/user_polymerize_discard/delAll', user_polymerize_discard.deleteAll),
    path('api/user_polymerize_discard/getList', user_polymerize_discard.getList),

    # 推广明细
    path('api/user_promotion_detail/addList', user_promotion_detail.addList),
    path('api/user_promotion_detail/del', user_promotion_detail.delete),
    path('api/user_promotion_detail/getList', user_promotion_detail.getList),

    # 推广
    path('api/user_promotion/addList', user_promotion.addList),
    path('api/user_promotion/del', user_promotion.delete),
    path('api/user_promotion/getList', user_promotion.getList),

    # 采购
    path('api/user_purchase/addList', user_purchase.addList),
    path('api/user_purchase/del', user_purchase.delete),
    path('api/user_purchase/getList', user_purchase.getList),

    # 退货
    path('api/user_refund/addList', user_refund.addList),
    path('api/user_refund/del', user_refund.delete),
    path('api/user_refund/getList', user_refund.getList),

    # 小额打款
    path('api/user_transfer/addList', user_transfer.addList),
    path('api/user_transfer/del', user_transfer.delete),
    path('api/user_transfer/getList', user_transfer.getList),
]
