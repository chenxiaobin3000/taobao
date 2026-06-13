# 商品状态
class GoodStatus:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    SALE = 1    # 在售
    REMOVE = 2  # 下架
    DELETE = 3  # 删除
    OTHER = 4   # 异常

    @staticmethod
    def num2text(value):
        return {
            GoodStatus.SALE: '在售',
            GoodStatus.REMOVE: '下架',
            GoodStatus.DELETE: '删除'
        }.get(value, '异常')
