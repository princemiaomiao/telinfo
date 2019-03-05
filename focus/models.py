# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


class PostManager(models.Manager):

    def query_by_column(self, category_id):
        query = self.get_queryset().filter(category_id=category_id)
        return query

    def query_by_user(self, user_id):
        user = User.objects.get(id=user_id)
        article_list = user.article_set.all()
        return article_list

    def query_by_polls(self):
        query = self.get_queryset().order_by('views')
        return query

    def query_by_time(self):
        query = self.get_queryset().order_by('-pub_date')
        return query

    def query_by_keyword(self, keyword):
        query = self.get_queryset().filter(title__contains=keyword)
        return query


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('category_name', max_length=256)
    intro = models.TextField('introduction', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'category'
        ordering = ['name']


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    category = models.ForeignKey(Category, verbose_name='belong to')
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=256)

    record_id = models.CharField(max_length=14)
    company_name = models.CharField(max_length=256)
    tel_no = models.CharField(max_length=20)
    consultee = models.CharField(max_length=20, blank=True)
    content = models.TextField('content')
    assign_person = models.CharField(max_length=20, blank=True)
    result = models.CharField(max_length=50, blank=True)
    pricing = models.CharField(max_length=20, blank=True)
    published = models.BooleanField('notDraft', default=False)
    author = models.ForeignKey(User, verbose_name="user")
    pub_date = models.DateTimeField(auto_now_add=True, editable=True)
    update_time = models.DateTimeField(auto_now=True, null=True)
    remarks = models.TextField('remarks', blank=True)

    excerpt = models.CharField(max_length=200, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

        # 自定义 get_absolute_url 方法
        # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
            return reverse('focus:detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'post'
        ordering = ['-pub_date']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.content))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    objects = PostManager()


class PostQueryset(models.QuerySet):

    def visible(self):
        return self.filter(hidden=False)
