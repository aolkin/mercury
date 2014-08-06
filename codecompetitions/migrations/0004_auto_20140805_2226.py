# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0003_auto_20140805_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='language',
            old_name='index',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=80, default='Will be auto-populated', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='language',
            name='version',
            field=models.CharField(max_length=160, default='Will be auto-populated', null=True, blank=True),
        ),
    ]
