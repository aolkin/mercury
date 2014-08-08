# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0013_auto_20140807_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='auto_judge',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
