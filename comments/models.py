# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


# python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey('focus.Post', null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.content
