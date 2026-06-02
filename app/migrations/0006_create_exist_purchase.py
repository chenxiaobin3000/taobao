from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_add_purchase_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExistPurchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.IntegerField(db_index=True)),
                ('purchase_id', models.CharField(db_index=True, max_length=20)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 't_exist_purchase',
            },
        ),
    ]
