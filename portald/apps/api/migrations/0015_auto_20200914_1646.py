# Generated by Django 3.1 on 2020-09-14 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20200914_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='comments',
            field=models.ManyToManyField(blank=True, null=True, to='api.Comment'),
        ),
    ]
