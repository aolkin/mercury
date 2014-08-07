# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import codecompetitions.models


class Migration(migrations.Migration):

    dependencies = [
        ('codecompetitions', '0008_auto_20140806_0032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ('start_time', 'date_created')},
        ),
        migrations.AlterField(
            model_name='extrafile',
            name='file',
            field=models.FileField(max_length=160, upload_to=codecompetitions.models.get_run_fn_extra, storage=django.core.files.storage.FileSystemStorage(base_url='/private', location='/home/aaron/intranet/privatefiles')),
        ),
        migrations.AlterField(
            model_name='run',
            name='main_file',
            field=models.FileField(max_length=160, upload_to=codecompetitions.models.get_run_fn, storage=django.core.files.storage.FileSystemStorage(base_url='/private', location='/home/aaron/intranet/privatefiles')),
        ),
    ]
