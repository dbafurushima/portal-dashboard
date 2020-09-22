# Generated by Django 3.1 on 2020-09-14 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200914_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='note',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.note'),
        ),
    ]