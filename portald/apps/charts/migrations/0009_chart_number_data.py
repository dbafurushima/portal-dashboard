# Generated by Django 3.1 on 2020-11-17 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0008_chart_from_zabbix'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='number_data',
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
    ]
