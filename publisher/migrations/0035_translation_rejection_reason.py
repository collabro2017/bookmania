# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0034_auto_20170508_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='translation',
            name='rejection_reason',
            field=models.TextField(default=b''),
        ),
    ]
