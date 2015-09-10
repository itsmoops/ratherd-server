# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rathers', '0003_auto_20150804_1823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rather',
            old_name='vote_no',
            new_name='losses',
        ),
        migrations.RenameField(
            model_name='rather',
            old_name='vote_yes',
            new_name='wins',
        ),
    ]
