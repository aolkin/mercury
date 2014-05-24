# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_auto_20140520_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='image',
            field=models.ImageField(blank=True, upload_to='voting_images/%Y-%m/', null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, upload_to='voting_images/%Y-%m/', null=True),
        ),
        migrations.AlterField(
            model_name='choice',
            name='image',
            field=models.ImageField(blank=True, upload_to='voting_images/%Y-%m/', null=True),
        ),
    ]
