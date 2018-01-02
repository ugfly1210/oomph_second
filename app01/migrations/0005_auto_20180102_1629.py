# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
        ('app01', '0004_auto_20171227_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='auth',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.User', verbose_name='用户权限'),
        ),
        migrations.AlterField(
            model_name='salerank',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='课程顾问'),
        ),
    ]