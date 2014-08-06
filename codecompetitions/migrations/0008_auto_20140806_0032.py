# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.files.storage
import codecompetitions.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codecompetitions', '0007_auto_20140805_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('file', models.FileField(max_length=160, storage=django.core.files.storage.FileSystemStorage(location='/home/aaron/intranet/privatefiles', base_url=''), upload_to=codecompetitions.models.get_run_fn_extra)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Run',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('number', models.PositiveSmallIntegerField()),
                ('is_a_test', models.BooleanField(default=False)),
                ('main_file', models.FileField(max_length=160, storage=django.core.files.storage.FileSystemStorage(location='/home/aaron/intranet/privatefiles', base_url=''), upload_to=codecompetitions.models.get_run_fn)),
                ('has_been_run', models.BooleanField(default=False)),
                ('output', models.TextField(null=True, blank=True)),
                ('runtime', models.PositiveIntegerField(null=True, help_text='in milliseconds', blank=True)),
                ('exit_code', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('time_to_submission', models.PositiveIntegerField(null=True, help_text='in milliseconds, though not accurate to the millisecond', blank=True)),
                ('time_of_submission', models.DateTimeField(auto_now_add=True)),
                ('judgement', models.CharField(max_length=120, null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('score', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('language', models.ForeignKey(to='codecompetitions.Language')),
                ('problem', models.ForeignKey(to='codecompetitions.Problem')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='extrafile',
            name='run',
            field=models.ForeignKey(to='codecompetitions.Run'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='competition',
            name='original_time_left',
            field=models.PositiveIntegerField(help_text='in seconds'),
        ),
        migrations.AlterField(
            model_name='competition',
            name='paused_time_left',
            field=models.PositiveIntegerField(null=True, help_text='in seconds', blank=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='read_from_file',
            field=models.CharField(max_length=80, null=True, help_text="If specified, the input data will be placed into a file with this name in the same directory as the player's code.", blank=True),
        ),
        migrations.AlterField(
            model_name='problem',
            name='time_limit',
            field=models.PositiveIntegerField(help_text='in seconds', default=5),
        ),
    ]
