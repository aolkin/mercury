# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0015_auto_20140809_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='sample_input_data',
            field=models.TextField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='competition',
            name='admins',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='admin_users'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='judges',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='judge_users'),
        ),
    ]
