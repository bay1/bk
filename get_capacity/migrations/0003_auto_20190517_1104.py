# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-17 11:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('get_capacity', '0002_memoryusage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diskusage',
            old_name='disk_usage',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='memoryusage',
            old_name='memory_usage',
            new_name='value',
        ),
    ]