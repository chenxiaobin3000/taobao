# 商品类型
class GoodType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    NORMAL = 1      # 商品
    GIFT = 2        # 赠品
    SUPPLEMENT = 3  # 补差价
    OTHER = 4       # 异常

    @staticmethod
    def num2text(value):
        return {
            GoodType.NORMAL: '商品',
            GoodType.GIFT: '赠品',
            GoodType.SUPPLEMENT: '补差价'
        }.get(value, '异常')
