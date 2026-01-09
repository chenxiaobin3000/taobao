# 退货状态
class RefundStatus:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    SUCCESS = 1  # 退款成功
    CLOSE = 2    # 退款关闭
    APPLY = 3    # 买家已经申请退款，等待卖家同意
    AGREE = 4    # 卖家已经同意退款，等待买家退货
    SHIPPED = 5  # 买家已经退货，等待卖家确认收货
    EXCHANGE = 6 # 卖家已发货,等待卖家和买家确认收货
    AGAIN = 7    # 等待买家确认重新邮寄的货物
    OTHER = 8    # 异常
