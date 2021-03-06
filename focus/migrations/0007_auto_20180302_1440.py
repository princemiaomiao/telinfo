# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-02 06:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0006_auto_20180302_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='assign_person',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='focus.Category', verbose_name='belong to'),
        ),
        migrations.AlterField(
            model_name='post',
            name='consultee',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='pricing',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='post',
            name='result',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
