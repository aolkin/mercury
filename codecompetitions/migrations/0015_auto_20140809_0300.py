# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0014_problem_auto_judge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='time_to_submission',
            field=models.PositiveIntegerField(help_text='in seconds', null=True, blank=True),
        ),
    ]
