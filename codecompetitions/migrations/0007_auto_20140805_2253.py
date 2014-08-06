# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0006_auto_20140805_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='expected_output',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='input_data',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='problem',
            name='read_from_file',
            field=models.CharField(blank=True, null=True, max_length=80),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='problem',
            name='time_limit',
            field=models.PositiveIntegerField(default=5),
            preserve_default=True,
        ),
    ]
