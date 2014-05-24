# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('key', models.CharField(unique=True, max_length=40, primary_key=True, serialize=False)),
                ('value', models.CharField(max_length=240, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
