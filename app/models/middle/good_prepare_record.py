from datetime import timedelta

from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone

from app.models.system.shop import Shop
from app.models.system.user import User
from app.models.system.user_shop import UserShop


class GoodPrepareRecordManager(models.Manager):
    def getUserShops(self, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return []
        shop_ids = UserShop.objects.filter(user_id=user_id).values_list('shop_id', flat=True)
        return list(
            Shop.objects.filter(company_id=user.company_id, id__in=shop_ids)
            .order_by('id')
            .values('id', 'name')
        )

    def getValidShopIds(self, user_id, shop_ids=None):
        valid_ids = [shop['id'] for shop in self.getUserShops(user_id)]
        if shop_ids is None:
            return valid_ids
        shop_ids = [int(shop_id) for shop_id in shop_ids]
        return [shop_id for shop_id in shop_ids if shop_id in valid_ids]

    def set(self, user_id, shop_ids, prepare_date, prepare_detail, harvest_date, record_note):
        valid_ids = self.getValidShopIds(user_id, shop_ids)
        if len(valid_ids) != len(shop_ids):
            return False
        for shop_id in valid_ids:
            self.update_or_create(
                shop_id=shop_id,
                prepare_date=prepare_date,
                defaults={
                    'prepare_detail': prepare_detail,
                    'harvest_date': harvest_date or None,
                    'record_note': record_note
                }
            )
        return True

    def clear(self, user_id, shop_ids, prepare_date):
        valid_ids = self.getValidShopIds(user_id, shop_ids)
        if len(valid_ids) != len(shop_ids):
            return False
        self.filter(shop_id__in=valid_ids, prepare_date=prepare_date).delete()
        return True

    def getList(self, user_id, shop_id, start_date, end_date):
        shops = self.getUserShops(user_id)
        if shop_id:
            shops = [shop for shop in shops if shop['id'] == shop_id]

        shop_map = {shop['id']: shop['name'] for shop in shops}
        if not shop_map:
            return []

        records = list(self.filter(
            shop_id__in=shop_map.keys(),
            prepare_date__gte=start_date,
            prepare_date__lte=end_date
        ).order_by('shop_id'))
        records_by_date = {}
        for record in records:
            records_by_date.setdefault(record.prepare_date, []).append(record)

        datas = []
        current = end_date
        while current >= start_date:
            date_records = records_by_date.get(current, [])
            shop_ids = [record.shop_id for record in date_records]
            datas.append({
                'id': date_records[0].id if date_records else 0,
                'shop_ids': shop_ids,
                'shop_name': ','.join([shop_map[shop_id] for shop_id in shop_ids]),
                'prepare_date': current,
                'prepare_detail': self.joinValues([record.prepare_detail for record in date_records]),
                'harvest_date': self.joinValues([record.harvest_date for record in date_records]),
                'record_note': self.joinValues([record.record_note for record in date_records]),
                'edit_prepare_detail': self.sameValue([record.prepare_detail for record in date_records]),
                'edit_harvest_date': self.sameValue([record.harvest_date for record in date_records]),
                'edit_record_note': self.sameValue([record.record_note for record in date_records])
            })
            current -= timedelta(days=1)
        return datas

    def joinValues(self, values):
        datas = []
        for value in values:
            if value is None or value == '':
                continue
            text = str(value)
            if text not in datas:
                datas.append(text)
        return ','.join(datas)

    def sameValue(self, values):
        values = [value for value in values if value is not None and value != '']
        if not values:
            return ''
        first = values[0]
        if all(value == first for value in values):
            return first
        return ''

    def encoder(self, record):
        if record:
            return model_to_dict(record, fields=[
                'id',
                'shop_id',
                'prepare_detail',
                'prepare_date',
                'harvest_date',
                'record_note'
            ])
        return None


class GoodPrepareRecord(models.Model):
    objects = GoodPrepareRecordManager()
    shop_id = models.IntegerField(db_index=True)
    prepare_detail = models.CharField(max_length=20)
    prepare_date = models.DateField(db_index=True)
    harvest_date = models.DateField(null=True, blank=True)
    record_note = models.CharField(max_length=20)
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_good_prepare_record'
        unique_together = ('shop_id', 'prepare_date')
