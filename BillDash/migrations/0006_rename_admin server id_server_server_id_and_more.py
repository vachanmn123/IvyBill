# Generated by Django 4.0.6 on 2022-08-04 06:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BillDash', '0005_plan_server_next_payment_date_payment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='Admin Server ID',
            new_name='server_id',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='Server ID',
            new_name='server_id_hex',
        ),
    ]
