# Generated by Django 3.1 on 2020-09-14 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20200908_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=60, verbose_name='Endereço'),
        ),
    ]