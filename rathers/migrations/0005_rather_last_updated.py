# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rathers', '0004_auto_20150804_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='rather',
            name='last_updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 21, 31, 52, 37095, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
