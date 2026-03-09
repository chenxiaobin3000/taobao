# 财务类型
class FinanceType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")

    MARGIN = 1      # 保证金
    SHARE = 2       # 分账
    ONLINE = 3      # 在线支付
    TRANSFER = 4    # 转账
    REFUND = 5      # 退款
    OTHER = 6       # 其他
    DEDUCTION = 7   # 扣款
    COLLECTION = 8  # 交易收款
    CASH = 9        # 提现
    ERROR = 10      # 异常
