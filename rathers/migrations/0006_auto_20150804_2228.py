# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rathers', '0005_rather_last_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rather',
            old_name='last_updated',
            new_name='date_updated',
        ),
    ]
