# Generated by Django 3.1.7 on 2021-04-05 22:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Tópico',
                'verbose_name_plural': 'Tópicos',
            },
        ),
        migrations.CreateModel(
            name='AppNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True, verbose_name='Titulo')),
                ('text', models.CharField(max_length=250, verbose_name='Texto')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('favorite', models.BooleanField(blank=True, default=True, null=True, verbose_name='Favorito')),
                ('display', models.BooleanField(blank=True, default=True, null=True, verbose_name='Visível')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='portal.topic')),
            ],
            options={
                'verbose_name': 'Anotação',
                'verbose_name_plural': 'Anotações',
            },
        ),
    ]