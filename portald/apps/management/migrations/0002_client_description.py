# Generated by Django 3.1.5 on 2021-01-15 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
