from django.db import models
from django.utils import timezone


class ReceiptMapManager(models.Manager):
    def set(self, item_id, map_id):
        receipt_map, _ = self.update_or_create(
            item_id=item_id,
            defaults={'map_id': map_id}
        )
        return receipt_map

    def getMap(self):
        return dict(self.values_list('item_id', 'map_id'))


class ReceiptMap(models.Model):
    objects = ReceiptMapManager()
    item_id = models.IntegerField(db_index=True, unique=True)
    map_id = models.IntegerField(db_index=True)
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_receipt_map'
