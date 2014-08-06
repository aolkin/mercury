# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0005_auto_20140805_2228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ('index',)},
        ),
        migrations.AddField(
            model_name='competition',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.date(2014, 8, 5)),
            preserve_default=False,
        ),
    ]
