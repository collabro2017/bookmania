# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0012_bookpage_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='processing_completed',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookimage',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='publisher.Book'),
        ),
        migrations.AlterField(
            model_name='bookpage',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='publisher.Book'),
        ),
    ]
