# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_choice'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('user', models.ForeignKey(to_field='id', to=settings.AUTH_USER_MODEL)),
                ('choice', models.ForeignKey(to_field='id', to='voting.Choice')),
                ('question', models.ForeignKey(to_field='id', to='voting.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
