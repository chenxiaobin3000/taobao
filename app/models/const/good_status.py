# 商品状态
class GoodType:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    SALE = 1    # 在售
    REMOVE = 2  # 下架
    DELETE = 3  # 删除
    OTHER = 4   # 异常
