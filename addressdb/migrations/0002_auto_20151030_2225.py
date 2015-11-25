# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address2',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address3',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='address4',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='extra_info',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='secondary_phone1',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='secondary_phone2',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
