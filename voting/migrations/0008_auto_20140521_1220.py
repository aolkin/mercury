# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0007_auto_20140520_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='enabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='poll',
            name='viewers',
            field=models.ManyToManyField(null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
