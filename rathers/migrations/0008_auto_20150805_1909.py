# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rathers', '0007_rather_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rather',
            name='ratio',
            field=models.DecimalField(default=0.5, max_digits=20, decimal_places=10),
        ),
    ]
