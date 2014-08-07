# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0009_auto_20140806_1238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ('start_time', 'date_modified')},
        ),
        migrations.AddField(
            model_name='competition',
            name='date_modified',
            field=models.DateTimeField(default=datetime.date(2014, 8, 6), auto_now=True),
            preserve_default=False,
        ),
    ]
