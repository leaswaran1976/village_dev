# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressdb', '0006_auto_20151123_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='relation',
            field=models.CharField(max_length=30, blank=True, null=True),
        ),
    ]
