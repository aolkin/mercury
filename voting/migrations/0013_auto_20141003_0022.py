# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0012_auto_20140526_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='viewers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True, related_name='view_only_users'),
        ),
    ]
