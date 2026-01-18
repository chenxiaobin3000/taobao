# 商品类型
class GoodType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    NORMAL = 1 # 普通商品
    GIFT = 2   # 赠品
    OTHER = 3  # 异常
