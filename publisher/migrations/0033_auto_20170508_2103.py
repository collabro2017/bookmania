# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-08 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0032_auto_20170508_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layouttemplate',
            name='publisher',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='publisher.Publisher'),
        ),
    ]