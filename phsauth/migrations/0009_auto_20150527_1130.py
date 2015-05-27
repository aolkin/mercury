# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('phsauth', '0008_auto_20141003_0022'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ldapuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='student',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='teacher',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
