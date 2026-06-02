from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_create_exist_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='existpurchase',
            name='purchase_id',
            field=models.CharField(db_index=True, max_length=20, unique=True),
        ),
    ]
