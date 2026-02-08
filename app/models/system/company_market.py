from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 公司-平台关系表
class CompanyMarketManager(models.Manager):
    def add(self, company_id, market_id):
        return self.create(company_id=company_id, market_id=market_id)

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def total(self, company_id):
        return self.filter(company_id=company_id).count()

    def getList(self, company_id, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(self.filter(company_id=company_id)[left:right])

    def encoderList(self, companyMarkets):
        if companyMarkets:
            return [model_to_dict(companyMarket, fields=['id', 'company_id', 'market_id']) for companyMarket in companyMarkets]
        return None
    
class CompanyMarket(models.Model):
    objects = CompanyMarketManager()
    company_id = models.IntegerField(db_index = True) # 公司id
    market_id = models.IntegerField(db_index = True) # 平台id
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_company_market'
