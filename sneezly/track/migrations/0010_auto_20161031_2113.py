# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-31 20:13
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0009_auto_20161031_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attrs',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='attr_schema',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]
