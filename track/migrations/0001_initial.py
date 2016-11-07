# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 17:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True, unique=True)),
                ('soap_type', models.CharField(blank=True, choices=[('DV', 'Dove'), ('SM', 'Simple'), ('NN', 'None')], default='SM', max_length=2)),
                ('shower_temp', models.CharField(blank=True, choices=[('HO', 'Hot'), ('WA', 'Warm'), ('CO', 'Cold')], default='HO', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='track.EventType'),
        ),
    ]