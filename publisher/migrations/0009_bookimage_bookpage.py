# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 18:52
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import publisher.models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0008_book_cover_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, null=True, upload_to=publisher.models.book_image_path)),
                ('thumbnail', imagekit.models.fields.ProcessedImageField(default=None, null=True, upload_to=publisher.models.book_image_path)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publisher.Book')),
            ],
        ),
        migrations.CreateModel(
            name='BookPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'flagged', b'flagged'), (b'published', b'published'), (b'pending', b'pending'), (b'draft', b'draft')], default=b'draft', max_length=30)),
                ('content', models.TextField(default=b'')),
                ('raw_content', models.TextField(default=b'')),
                ('layout', django.contrib.postgres.fields.jsonb.JSONField(default=None, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publisher.Book')),
            ],
        ),
    ]