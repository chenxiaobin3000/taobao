# 商品进货类型
class GoodStockType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    ALIBABA = 1      # 1688
    TAO_BAO = 2      # 淘宝
    PIN_DUO_DUO = 3  # 拼多多
    DOU_YIN = 4      # 抖音
    OTHER = 5        # 异常
