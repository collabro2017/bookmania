# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-07 21:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0003_remove_publisher_users'),
        ('users', '0002_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='publisher',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='publisher.Publisher'),
        ),
    ]
