# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0011_question_choice_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='choice_extra',
            field=models.CharField(blank=True, max_length=512, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='response',
            name='choice',
            field=models.ForeignKey(blank=True, null=True, to_field='id', to='voting.Choice'),
        ),
    ]
