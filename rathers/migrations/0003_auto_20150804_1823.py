# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rathers', '0002_rather_paired_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rather',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
