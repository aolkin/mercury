# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('begin_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('allow_edits', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=80)),
                ('desc', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to='voting_images/%Y-%m/polls')),
                ('display_mode', models.PositiveSmallIntegerField()),
                ('admins', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('viewers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('restrict_to', models.ManyToManyField(to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
