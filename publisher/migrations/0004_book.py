# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 16:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import publisher.models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0003_remove_publisher_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(b'flagged', b'flagged'), (b'published', b'published'), (b'pending', b'pending'), (b'draft', b'draft')], default=b'draft', max_length=30)),
                ('name', models.CharField(default=b'', max_length=50)),
                ('description', models.TextField(default=b'')),
                ('cover_image', models.ImageField(default=None, null=True, upload_to=publisher.models.book_image_path)),
                ('book_pdf', models.FileField(default=None, null=True, upload_to=publisher.models.book_pdf_path)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publisher.Publisher')),
            ],
        ),
    ]
