# Generated by Django 3.1 on 2020-08-27 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200826_1643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='ip',
        ),
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='subject'),
        ),
    ]
