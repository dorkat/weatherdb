# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercise2', '0002_auto_20150902_0810'),
    ]

    operations = [
        migrations.DeleteModel(
            name='City_Temperature_Table',
        ),
    ]
