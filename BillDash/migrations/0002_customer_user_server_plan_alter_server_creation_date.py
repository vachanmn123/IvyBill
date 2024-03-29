# Generated by Django 4.0.6 on 2022-07-28 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BillDash', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='server',
            name='plan',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='server',
            name='creation_date',
            field=models.TimeField(auto_now=True),
        ),
    ]
