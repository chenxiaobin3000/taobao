from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_existpurchase_purchase_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='existpurchase',
            name='purchase_id',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
