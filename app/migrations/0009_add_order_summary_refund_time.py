from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_existpurchase_purchase_id_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordersummary',
            name='refund_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
