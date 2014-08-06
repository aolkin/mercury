# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='paused_time_left',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
