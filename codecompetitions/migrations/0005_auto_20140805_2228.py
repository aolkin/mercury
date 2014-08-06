# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0004_auto_20140805_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='language',
            old_name='id',
            new_name='index',
        ),
    ]
