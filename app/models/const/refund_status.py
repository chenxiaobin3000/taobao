# 退货状态
class RefundStatus:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    SUCCESS = 1 # 退款成功
    CLOSE = 2   # 退款关闭
    SHIPPED = 3 # 买家已退货，等待卖家收货
    AGREE = 4   # 卖家已同意，等待买家退货
    OTHER = 5  # 异常
