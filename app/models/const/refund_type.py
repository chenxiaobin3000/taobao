# 退款类型
class RefundType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    REFUND = 1   # 仅退款
    RETURN = 2   # 退货退款
    EXCHANGE = 3 # 换货
    OTHER = 4    # 异常
