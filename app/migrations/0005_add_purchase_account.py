from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_purchase_shop_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpurchase',
            name='purchase_account',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AddField(
            model_name='purchase',
            name='purchase_account',
            field=models.CharField(default='', max_length=16),
        ),
    ]
