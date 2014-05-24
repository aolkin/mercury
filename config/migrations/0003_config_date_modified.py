# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_config_missing'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='date_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2014, 5, 23, 18, 2, 48, 967159)),
            preserve_default=False,
        ),
    ]
