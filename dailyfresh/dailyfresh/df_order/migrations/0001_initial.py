# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
        ('df_cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order_id', models.CharField(max_length=10)),
                ('isPay', models.BooleanField(default=False)),
                ('cart', models.ForeignKey(to='df_cart.CarInfo')),
                ('user', models.ForeignKey(to='df_user.userInfo')),
            ],
        ),
    ]
