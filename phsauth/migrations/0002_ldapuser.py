# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('phsauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LDAPUser',
            fields=[
                ('user_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, to=settings.AUTH_USER_MODEL, to_field='id')),
                ('dn', models.CharField(null=True, max_length=160)),
                ('kind', models.CharField(null=True, max_length=80)),
                ('home_dir', models.CharField(null=True, max_length=160)),
            ],
            options={
                'verbose_name': 'LDAP User',
            },
            bases=('auth.user',),
        ),
    ]
