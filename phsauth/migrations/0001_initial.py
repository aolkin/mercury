# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LDAPGroup',
            fields=[
                ('group_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, to='auth.Group', to_field='id')),
                ('dn', models.CharField(max_length=160)),
            ],
            options={
                'verbose_name': 'LDAP Security Group',
            },
            bases=('auth.group',),
        ),
    ]
