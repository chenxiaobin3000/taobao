# 推广类型
class PromotionType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    CAR = 1    # 直通车
    WHOLE = 2  # 全站
    PEOPLE = 3 # 人群
    PREPAYMENT = 4 # 下单金额被预支付扣款
    OTHER = 5  # 异常
