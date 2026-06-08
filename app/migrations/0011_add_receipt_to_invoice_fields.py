from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_add_receipt_from_invoice_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptto',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='receiptto',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='receiptto',
            name='tax_rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='receiptto',
            name='company',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='receiptto',
            name='company_id',
            field=models.CharField(default='', max_length=20),
        ),
    ]
