# Generated by Django 3.1 on 2020-08-27 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200827_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='message',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
