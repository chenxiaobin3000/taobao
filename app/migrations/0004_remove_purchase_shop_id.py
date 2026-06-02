from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_purchase_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpurchase',
            name='shop_id',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='shop_id',
        ),
    ]
