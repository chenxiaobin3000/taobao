from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_receipt_to_old_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=20)),
                ('company_id', models.CharField(max_length=20)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 't_receipt_owner',
            },
        ),
    ]
