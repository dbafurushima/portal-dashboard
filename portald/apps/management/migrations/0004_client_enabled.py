# Generated by Django 3.1.7 on 2021-03-31 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_auto_20210209_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='enabled',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Habilitado'),
        ),
    ]
