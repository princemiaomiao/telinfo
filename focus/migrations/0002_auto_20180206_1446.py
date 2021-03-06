# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-06 06:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('focus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='category_name')),
                ('intro', models.TextField(default='', verbose_name='introduction')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'category',
                'verbose_name_plural': 'category',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='column',
        ),
        migrations.DeleteModel(
            name='Column',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Category', verbose_name='belong to'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, to='focus.Tag'),
        ),
    ]
