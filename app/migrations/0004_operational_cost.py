from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_receipt_map'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationalCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateField(db_index=True)),
                ('user_id', models.IntegerField(db_index=True)),
                ('project_name', models.CharField(db_index=True, max_length=32)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('cost_note', models.CharField(max_length=32)),
                ('ctime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 't_operational_cost',
            },
        ),
    ]
