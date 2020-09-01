# Generated by Django 3.1 on 2020-09-01 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('os_name', models.CharField(max_length=40, verbose_name='os.name')),
                ('arch', models.CharField(max_length=30, verbose_name='arch')),
                ('platform', models.CharField(max_length=30, verbose_name='platform')),
                ('processor', models.CharField(max_length=80)),
                ('hostname', models.CharField(max_length=125)),
                ('ram', models.FloatField(verbose_name='RAM')),
                ('physical_cores', models.IntegerField(verbose_name='physical cores')),
                ('current_frequency', models.FloatField(verbose_name='current frequency')),
            ],
        ),
        migrations.CreateModel(
            name='Locator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locator', models.CharField(max_length=20)),
                ('size', models.IntegerField(blank=True, null=True)),
                ('speed', models.IntegerField(blank=True, null=True)),
                ('host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.host')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('equipment', models.CharField(choices=[('virtual', 'Virtual Machine'), ('real', 'Physical Machine'), ('docker', 'Container Docker')], max_length=30, verbose_name='equipamento')),
                ('host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.host')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('host', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.host')),
            ],
        ),
    ]
