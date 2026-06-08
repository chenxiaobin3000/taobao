from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_add_order_summary_refund_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptfrom',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='receiptfrom',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='receiptfrom',
            name='tax_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='receiptfrom',
            name='company',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='receiptfrom',
            name='company_id',
            field=models.CharField(default='', max_length=20),
        ),
    ]
