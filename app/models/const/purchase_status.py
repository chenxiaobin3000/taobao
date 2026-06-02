# 采购状态
class PurchaseStatus:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")

    SUCCESS = 1  # 交易成功
    CLOSE = 2    # 交易关闭
    OTHER = 3    # 异常
