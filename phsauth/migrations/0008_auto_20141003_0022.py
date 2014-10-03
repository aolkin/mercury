# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('phsauth', '0007_ldapgroup_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ldapgroup',
            name='group_ptr',
            field=models.OneToOneField(primary_key=True, parent_link=True, to='auth.Group', serialize=False, auto_created=True),
        ),
        migrations.AlterField(
            model_name='ldapuser',
            name='user_ptr',
            field=models.OneToOneField(primary_key=True, parent_link=True, to=settings.AUTH_USER_MODEL, serialize=False, auto_created=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='hr',
            field=models.ForeignKey(null=True, blank=True, to='phsauth.LDAPGroup', related_name='student_hr'),
        ),
        migrations.AlterField(
            model_name='student',
            name='ldapuser_ptr',
            field=models.OneToOneField(primary_key=True, parent_link=True, to='phsauth.LDAPUser', serialize=False, auto_created=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='school',
            field=models.ForeignKey(null=True, blank=True, to='phsauth.LDAPGroup', related_name='student_school'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='ldapuser_ptr',
            field=models.OneToOneField(primary_key=True, parent_link=True, to='phsauth.LDAPUser', serialize=False, auto_created=True),
        ),
    ]
