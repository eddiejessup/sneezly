# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 14:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0005_auto_20161030_1519'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventAttribute',
            new_name='EventAttributeValue',
        ),
    ]
