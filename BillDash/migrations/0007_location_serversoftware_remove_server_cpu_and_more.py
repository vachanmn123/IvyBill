# Generated by Django 4.0.6 on 2022-08-09 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BillDash', '0006_rename_admin server id_server_server_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('ptero_id', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerSoftware',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('game_name', models.CharField(max_length=25)),
                ('ptero_nest_id', models.IntegerField()),
                ('ptero_egg_id', models.IntegerField()),
                ('docker_image', models.CharField(blank=True, max_length=25, null=True)),
                ('startup_command', models.CharField(blank=True, max_length=1000, null=True)),
                ('environment', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu',
        ),
        migrations.RemoveField(
            model_name='server',
            name='disk',
        ),
        migrations.RemoveField(
            model_name='server',
            name='ram',
        ),
        migrations.AddField(
            model_name='plan',
            name='dedicated_ip',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customer',
            name='ptero_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='location',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='BillDash.location'),
        ),
        migrations.AddField(
            model_name='server',
            name='server_software',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='BillDash.serversoftware'),
        ),
    ]