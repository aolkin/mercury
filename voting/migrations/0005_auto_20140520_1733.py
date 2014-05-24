# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choices',
            field=models.ManyToManyField(to='voting.Choice'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
    ]
