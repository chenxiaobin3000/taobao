# 公司状态
class CompanyStatus:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    NORMAL = 1 # 正常
    CLOSE = 2  # 停业
    OTHER = 3  # 异常
