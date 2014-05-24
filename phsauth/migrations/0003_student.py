# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phsauth', '0002_ldapuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('ldapuser_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, to='phsauth.LDAPUser', to_field='user_ptr')),
                ('graduation_year', models.PositiveSmallIntegerField(null=True)),
                ('sid', models.CharField(null=True, max_length=8)),
                ('school', models.CharField(blank=True, null=True, max_length=20)),
                ('hr', models.CharField(blank=True, null=True, max_length=20)),
            ],
            options={
                'verbose_name': 'Student',
            },
            bases=('phsauth.ldapuser',),
        ),
    ]
