from django.db import models
from django.utils import timezone
from django.forms.models import model_to_dict

# 平台表
class MarketManager(models.Manager):
    def add(self, name):
        return self.create(name=name)

    def set(self, pk, name):
        market = self.get(pk=pk)
        market.name = name
        return market.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def find(self, pk):
        return self.get(pk=pk)

    def total(self):
        return self.all().count()

    def getList(self, page, num):
        left = (page - 1) * num
        right = page * num
        return self.all()[left:right]

    def encoder(self, market):
        if market:
            return model_to_dict(market, fields=['id', 'company_id', 'market_id', 'name'])
        return None

    def encoderList(self, markets):
        if markets:
            return [model_to_dict(market, fields=['id', 'company_id', 'market_id', 'name']) for market in markets]
        return None
    
class Market(models.Model):
    objects = MarketManager()
    name = models.CharField(max_length = 8, db_index = True, unique = True)
    ctime = models.DateTimeField(default = timezone.now)

    class Meta(object):
        db_table = 't_market'
