# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-04 15:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_uploadfilemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='UploadFileModel',
        ),
    ]