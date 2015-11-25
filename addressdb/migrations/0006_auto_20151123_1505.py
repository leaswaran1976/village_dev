# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressdb', '0005_auto_20151115_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='country',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
