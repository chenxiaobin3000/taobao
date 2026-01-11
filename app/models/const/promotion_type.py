# 推广类型
class PromotionType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    CAR = 1 # 直通车
    WHOLE = 2 # 全站
    OTHER = 3  # 异常
