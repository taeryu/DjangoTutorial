# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-02 07:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_delete_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileTitle', models.TextField(default='')),
                ('file', models.FileField(null=True, upload_to='')),
            ],
        ),
    ]