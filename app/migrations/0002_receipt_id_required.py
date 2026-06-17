from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptfrom',
            name='receipt_id',
            field=models.CharField(db_index=True, default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receiptto',
            name='receipt_id',
            field=models.CharField(db_index=True, default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='receiptfrom',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='receiptfrom',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='receiptfrom',
            name='tax_rate',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='receiptfrom',
            name='company',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='receiptto',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='receiptto',
            name='tax',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='receiptto',
            name='tax_rate',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='receiptto',
            name='company',
            field=models.CharField(max_length=20),
        ),
    ]
