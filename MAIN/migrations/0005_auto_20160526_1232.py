# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 12:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MAIN', '0004_auto_20160525_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='fax',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='tel',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='website',
            field=models.TextField(blank=True),
        ),
    ]
