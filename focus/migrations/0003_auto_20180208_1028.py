# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-08 02:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('focus', '0002_auto_20180206_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('record_id', models.CharField(max_length=14)),
                ('company_name', models.CharField(max_length=256)),
                ('tel_no', models.CharField(max_length=20)),
                ('consultee', models.CharField(max_length=20)),
                ('content', models.TextField(verbose_name='content')),
                ('assign_person', models.CharField(max_length=20)),
                ('result', models.CharField(max_length=50)),
                ('pricing', models.CharField(max_length=20)),
                ('published', models.BooleanField(default=True, verbose_name='notDraft')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('remarks', models.TextField(verbose_name='remarks')),
                ('excerpt', models.CharField(blank=True, max_length=200)),
                ('views', models.PositiveIntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='focus.Category', verbose_name='belong to')),
                ('tags', models.ManyToManyField(blank=True, to='focus.Tag')),
            ],
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'post',
                'verbose_name_plural': 'post',
            },
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='article',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='newuser',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='article',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='poll',
            name='user',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='NewUser',
        ),
        migrations.DeleteModel(
            name='Poll',
        ),
    ]
