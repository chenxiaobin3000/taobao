# 商品外部类型
class GoodOriginType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    TAO_BAO = 1     # 淘宝
    TIAN_MAO = 2    # 天猫
    OTHER = 3       # 异常
