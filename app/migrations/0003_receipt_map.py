from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_receipt_id_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.IntegerField(db_index=True, unique=True)),
                ('map_id', models.IntegerField(db_index=True)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 't_receipt_map',
            },
        ),
    ]
