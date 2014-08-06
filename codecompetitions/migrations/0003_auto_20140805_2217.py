# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0002_auto_20140805_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='custom_help',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='language',
            name='index',
            field=models.PositiveSmallIntegerField(serialize=False, primary_key=True),
        ),
    ]
