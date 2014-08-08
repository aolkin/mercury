# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0011_auto_20140806_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='run',
            name='compiled_successfully',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
    ]
