# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressdb', '0002_auto_20151030_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='family_name',
            field=models.CharField(null=True, max_length=60, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='nick_name',
            field=models.CharField(null=True, max_length=60, blank=True),
        ),
    ]
