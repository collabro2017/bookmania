# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 18:49
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0019_bookcomment_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookpage',
            name='content',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={b'images': {}, b'layout': b'top_image', b'text': {}}, null=True),
        ),
    ]