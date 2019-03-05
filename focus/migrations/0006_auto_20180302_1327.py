# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-02 05:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0005_auto_20180212_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='assign_person',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Category', verbose_name='belong to'),
        ),
        migrations.AlterField(
            model_name='post',
            name='consultee',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='pricing',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.BooleanField(default=False, verbose_name='notDraft'),
        ),
        migrations.AlterField(
            model_name='post',
            name='remarks',
            field=models.TextField(null=True, verbose_name='remarks'),
        ),
        migrations.AlterField(
            model_name='post',
            name='result',
            field=models.CharField(max_length=50, null=True),
        ),
    ]