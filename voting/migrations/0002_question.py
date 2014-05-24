# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('poll', models.ForeignKey(to_field='id', to='voting.Poll')),
                ('kind', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=80)),
                ('desc', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to='voting_images/%Y-%m/questions')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
