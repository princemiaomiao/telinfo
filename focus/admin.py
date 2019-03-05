# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.db import models
from django import forms
from .models import Post, Category, Tag


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'post_id', 'pub_date', 'content')


class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 41,
                   'cols': 100
                   })},
    }
    list_display = ('title', 'pub_date')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'intro')


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
