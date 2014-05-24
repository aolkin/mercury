# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phsauth', '0003_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('ldapuser_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, to='phsauth.LDAPUser', to_field='user_ptr')),
            ],
            options={
                'verbose_name': 'Teacher',
            },
            bases=('phsauth.ldapuser',),
        ),
    ]
