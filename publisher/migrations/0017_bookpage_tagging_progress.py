# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 19:25
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0016_remove_bookpage_tagging_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookpage',
            name='tagging_progress',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]
