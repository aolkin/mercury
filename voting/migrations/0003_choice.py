# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('desc', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(upload_to='voting_images/%Y-%m/choices')),
                ('question', models.ManyToManyField(to='voting.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
