# 商品关注状态
class GoodFollowStatus:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    ALL = 1    # 全部
    HAS_FOLLOW = 2  # 已关注
    NOT_FOLLOW = 3  # 未关注
    OTHER = 4   # 异常
