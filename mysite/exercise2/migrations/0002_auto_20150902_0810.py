# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercise2', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='city_temperature_table',
            table='City_Temperature_Table',
        ),
    ]
