# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0008_auto_20140521_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='confirmation',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poll',
            name='display_mode',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Normal')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='kind',
            field=models.PositiveSmallIntegerField(default=0, choices=[(0, 'Highest Wins'), (1, 'IRV'), (2, 'Fill-in')]),
        ),
    ]
