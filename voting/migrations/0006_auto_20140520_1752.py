# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0005_auto_20140520_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='restrict_to',
            field=models.ManyToManyField(blank=True, null=True, to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='display_mode',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='image',
            field=models.ImageField(blank=True, upload_to='voting_images/%Y-%m/polls', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, upload_to='voting_images/%Y-%m/questions', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='kind',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='poll',
            name='begin_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='poll',
            name='viewers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
