# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rathers', '0006_auto_20150804_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='rather',
            name='ratio',
            field=models.DecimalField(default=0, max_digits=20, decimal_places=10),
        ),
    ]
