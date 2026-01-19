# 商品类型
class GoodType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    NORMAL = 1      # 商品
    GIFT = 2        # 赠品
    SUPPLEMENT = 3  # 补差价
    OTHER = 4       # 异常
