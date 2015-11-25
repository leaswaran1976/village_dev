# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('addressdb', '0004_auto_20151101_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='alternate_email',
            field=models.EmailField(max_length=50, default=datetime.datetime(2015, 11, 16, 2, 59, 3, 984606, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='father_name',
            field=models.CharField(null=True, blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name='person',
            name='mother_name',
            field=models.CharField(null=True, blank=True, max_length=60),
        ),
    ]
