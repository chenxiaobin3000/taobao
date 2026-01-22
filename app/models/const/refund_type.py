# 退款类型
class RefundType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    REFUND = 1   # 仅退款
    RETURN = 2   # 退货退款
    EXCHANGE = 3 # 换货
    RESEND = 4   # 补寄
    REFUND = 5   # 退款
    SHIPPED = 6  # 退运费
    REPAIR = 7   # 维修
    OTHER = 8    # 异常
