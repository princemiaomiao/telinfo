# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'post_id', 'pub_date', 'content')


# Register your models here.
admin.site.register(Comment, CommentAdmin)
