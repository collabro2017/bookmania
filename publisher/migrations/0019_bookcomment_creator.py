# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 19:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publisher', '0018_bookcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcomment',
            name='creator',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
