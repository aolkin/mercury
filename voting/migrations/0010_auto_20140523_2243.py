# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0009_auto_20140523_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='content_type',
            field=models.ForeignKey(to_field='id', null=True, to='contenttypes.ContentType', default=None, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choice',
            name='object_id',
            field=models.PositiveIntegerField(null=True, default=None, blank=True),
            preserve_default=True,
        ),
    ]
