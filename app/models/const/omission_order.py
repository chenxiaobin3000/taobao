# 遗漏订单
class OmissionOrder:
    def __setattr__(self, name, value):
        raise AttributeError("Cannot modify constant attribute.")
 
    VALUE = '0000000000000000000'
