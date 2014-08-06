# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competition',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True, null=True)),
                ('original_time_left', models.PositiveIntegerField()),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('paused_time_left', models.PositiveIntegerField()),
                ('admins', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('judges', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('limit_to', models.ManyToManyField(blank=True, null=True, to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('index', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=80, null=True)),
                ('version', models.CharField(blank=True, max_length=160, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='competition',
            name='allowed_languages',
            field=models.ManyToManyField(to='codecompetitions.Language'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True, null=True)),
                ('competition', models.ForeignKey(to='codecompetitions.Competition')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
