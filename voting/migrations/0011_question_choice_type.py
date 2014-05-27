# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0010_auto_20140523_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choice_type',
            field=models.ForeignKey(to='contenttypes.ContentType', null=True, blank=True, to_field='id'),
            preserve_default=True,
        ),
    ]
