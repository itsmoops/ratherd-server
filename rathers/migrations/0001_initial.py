# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rather',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rather_text', models.CharField(max_length=1000)),
                ('vote_yes', models.IntegerField(default=0)),
                ('vote_no', models.IntegerField(default=0)),
                ('is_pair', models.BooleanField(default=False)),
                ('date_submitted', models.DateTimeField()),
            ],
        ),
    ]
