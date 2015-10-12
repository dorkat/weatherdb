# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercise2', '0004_city_temperature_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city_temperature_table',
            name='id',
        ),
        migrations.AlterField(
            model_name='city_temperature_table',
            name='city_id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
