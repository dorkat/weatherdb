# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('city_id', models.AutoField(serialize=False, primary_key=True)),
                ('city_name', models.CharField(max_length=100)),
                ('country_id', models.CharField(max_length=45)),
                ('temperature', models.CharField(max_length=45, null=True, blank=True)),
                ('humidity', models.CharField(max_length=45, null=True, blank=True)),
                ('clouds', models.CharField(max_length=45, null=True, blank=True)),
                ('wind_speed', models.CharField(max_length=45, null=True, blank=True)),
                ('wind_deg', models.CharField(max_length=45, null=True, blank=True)),
                ('max_temp', models.CharField(max_length=45, null=True, blank=True)),
                ('min_temp', models.CharField(max_length=45, null=True, blank=True)),
                ('pressure', models.CharField(max_length=45, null=True, blank=True)),
                ('data_key', models.CharField(max_length=45, null=True, blank=True)),
                ('last_update', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'db_table': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Countries',
            fields=[
                ('country_id', models.AutoField(serialize=False, primary_key=True)),
                ('country_name', models.CharField(max_length=45, unique=True, null=True, blank=True)),
                ('country_full_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'countries',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cities',
            unique_together=set([('city_name', 'country_id')]),
        ),
    ]
