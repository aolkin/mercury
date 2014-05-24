# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phsauth', '0004_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='hr_group',
            field=models.ForeignKey(to_field='group_ptr', null=True, blank=True, to='phsauth.LDAPGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='school_group',
            field=models.ForeignKey(to_field='group_ptr', null=True, blank=True, to='phsauth.LDAPGroup'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='student',
            name='hr',
        ),
        migrations.RemoveField(
            model_name='student',
            name='school',
        ),
    ]
