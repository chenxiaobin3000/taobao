from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_userpurchase_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='order_id',
        ),
    ]
