# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-27 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDistribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='recv_data',
            field=models.DateField(blank=True, null=True, verbose_name='接单时间'),
        ),
    ]
