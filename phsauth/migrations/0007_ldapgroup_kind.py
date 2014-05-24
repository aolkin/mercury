# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phsauth', '0006_auto_20140521_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='ldapgroup',
            name='kind',
            field=models.CharField(max_length=80, blank=True, null=True, choices=[('hr', 'Homeroom'), ('school', 'School'), ('type', 'Type'), (None, 'Unknown')]),
            preserve_default=True,
        ),
    ]
