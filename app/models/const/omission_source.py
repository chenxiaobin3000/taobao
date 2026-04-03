# 遗漏来源
class OmissionSource:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    DEDUCTION = 1 # 扣费
    POLYMERIZE = 2  # 聚合
    OTHER = 3  # 异常
