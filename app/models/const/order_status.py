# 交易状态
class OrderStatus:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    SUCCESS = 1 # 交易成功
    CLOSE = 2   # 交易关闭
    SHIPPED = 3 # 已发货：卖家已发货，等待买家确认
    PAID = 4    # 未发货：买家已付款,等待卖家发货 5等待买家付款
    UNPAID = 5  # 未付款：等待买家付款
    OTHER = 6   # 异常
