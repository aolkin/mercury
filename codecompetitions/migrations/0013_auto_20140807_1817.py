# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0012_run_compiled_successfully'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='exit_code',
            field=models.SmallIntegerField(null=True, blank=True),
        ),
    ]
