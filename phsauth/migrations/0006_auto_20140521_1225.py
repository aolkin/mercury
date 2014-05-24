# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phsauth', '0005_auto_20140521_1224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='school_group',
            new_name='school',
        ),
        migrations.RenameField(
            model_name='student',
            old_name='hr_group',
            new_name='hr',
        ),
    ]
