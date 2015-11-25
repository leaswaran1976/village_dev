# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addressdb', '0003_auto_20151030_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='person',
            name='dob',
            field=models.DateTimeField(verbose_name='Date and Time of Birth'),
        ),
    ]
