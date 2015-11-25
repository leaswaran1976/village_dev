# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('address1', models.CharField(max_length=300)),
                ('address2', models.CharField(max_length=300)),
                ('address3', models.CharField(max_length=300)),
                ('address4', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('nick_name', models.CharField(max_length=60)),
                ('family_name', models.CharField(max_length=60)),
                ('gothram', models.CharField(max_length=60)),
                ('star', models.CharField(max_length=60)),
                ('gender', models.CharField(max_length=10)),
                ('blood_group', models.CharField(max_length=6)),
                ('dob', models.DateTimeField(verbose_name='date and time of birth')),
                ('email', models.EmailField(max_length=50)),
                ('primary_phone', models.CharField(max_length=20)),
                ('secondary_phone1', models.CharField(max_length=20)),
                ('secondary_phone2', models.CharField(max_length=20)),
                ('extra_info', models.CharField(max_length=1000)),
                ('address', models.ForeignKey(to='addressdb.Contact')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
