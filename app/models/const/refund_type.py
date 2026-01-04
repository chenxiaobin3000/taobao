# 退款状态
class RefundType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    REFUND = 1 # 仅退款
    RETURN = 2 # 退货退款
    OTHER = 3  # 异常
