# Generated by Django 4.0.6 on 2022-08-29 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BillDash', '0010_remove_bill_id_bill_bill_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='suspended',
            field=models.BooleanField(default=False),
        ),
    ]
