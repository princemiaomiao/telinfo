# -*- coding: utf-8 -*-
from django import template
from django.db.models.aggregates import Count
from six.moves.urllib.parse import urlencode, urlparse, parse_qs
from django.core.urlresolvers import reverse
from ..models import Post, Category, Tag
from django.db.models import Q
from django.contrib.auth.models import Group

register = template.Library()


@register.simple_tag
def get_recent_posts(request, num=5):
    if is_viewer(request.user, 'record_viewer'):
        return Post.objects.all()[:num]
    else:
        return Post.objects.filter(Q(author=request.user) | Q(published='1'))[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('pub_date', 'month', order='DESC')


@register.simple_tag
def get_categories(request):
    # 记得在顶部引入 count 函数
    if is_viewer(request.user, 'record_viewer'):
        return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    else:
        return Category.objects.filter(Q(post__author=request.user) | Q(post__published='1')).annotate(
            num_posts=Count('post')).filter(Q(num_posts__gt=0))


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def change_url(request, kwargs=None, query=None):
    kwargs = kwargs or {}
    query = query or {}
    rm = request.resolver_match
    _kwargs = rm.kwargs.copy()
    _kwargs.update(kwargs)
    if _kwargs.get("page") == 1:
        _kwargs.pop('page', None)
    qs = parse_qs(urlparse(request.get_full_path()).query)
    qs.update(query)
    path = reverse(
        '%s:%s' % (rm.namespace, rm.url_name),
        args=rm.args,
        kwargs=_kwargs,
    )
    if qs:
        return "%s?%s" % (path, urlencode(qs, True))
    else:
        return path


@register.simple_tag
def change_post_ordering(request, ordering):
    return change_url(request, None, {'order': ordering})


@register.simple_tag
def change_page(request, page=1):
    return change_url(request, {"page": page})


@register.inclusion_tag('widgets/pagination.html', takes_context=True)
def get_pagination(context, first_last_amount=2, before_after_amount=4):
    page_obj = context['page_obj']
    paginator = context['paginator']
    is_paginated = context['is_paginated']
    page_numbers = []

    # Pages before current page
    if page_obj.number > first_last_amount + before_after_amount:
        for i in range(1, first_last_amount + 1):
            page_numbers.append(i)

        if first_last_amount + before_after_amount + 1 != paginator.num_pages:
            page_numbers.append(None)

        for i in range(page_obj.number - before_after_amount, page_obj.number):
            page_numbers.append(i)

    else:
        for i in range(1, page_obj.number):
            page_numbers.append(i)

    # Current page and pages after current page
    if page_obj.number + first_last_amount + before_after_amount < paginator.num_pages:
        for i in range(page_obj.number, page_obj.number + before_after_amount + 1):
            page_numbers.append(i)

        page_numbers.append(None)

        for i in range(paginator.num_pages - first_last_amount + 1, paginator.num_pages + 1):
            page_numbers.append(i)

    else:
        for i in range(page_obj.number, paginator.num_pages + 1):
            page_numbers.append(i)

    return {
        'paginator': paginator,
        'page_obj': page_obj,
        'page_numbers': page_numbers,
        'is_paginated': is_paginated,
        'request': context['request'],
    }


def is_viewer(user, group_name):
    try:
        if Group.objects.get(user=user).name == group_name:
            return True
        else:
            return False
    except Group.DoesNotExist:
        return False
