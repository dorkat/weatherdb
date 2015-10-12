# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercise2', '0003_delete_city_temperature_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='City_Temperature_Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city_id', models.IntegerField()),
            ],
            options={
                'db_table': 'City_Temperature_Table',
            },
        ),
    ]
