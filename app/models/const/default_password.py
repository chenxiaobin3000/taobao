# 默认密码
class DefaultPassword:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    # 系统默认密码:888888
    VALUE = '21218cca77804d2ba1922c33e0151105'
