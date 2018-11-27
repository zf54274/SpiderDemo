# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('u_name', models.CharField(max_length=20)),
                ('u_pwd', models.CharField(max_length=40)),
                ('u_email', models.CharField(max_length=30)),
                ('u_shou', models.CharField(max_length=30, default='')),
                ('u_address', models.CharField(max_length=100, default='')),
                ('u_youbian', models.CharField(max_length=6, default='')),
                ('u_phone', models.CharField(max_length=11, default='')),
            ],
        ),
    ]
