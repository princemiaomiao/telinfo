# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from .forms import LoginForm, PostForm, PostEditForm, StepOneForm
from .models import Post, Category, Tag
from comments.forms import CommentForm
from comments.models import Comment
from django.db.models import Q
from formtools.wizard.views import SessionWizardView

User = get_user_model()


# Create your views here.


class IndexView(ListView):
    model = Post
    template_name = 'view/index_new.html'
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super(IndexView, self).get_context_data(**kwargs)
        context['panel_title'] = 'New Posts'
        context['show_order'] = True
        if not is_viewer(self.request.user, 'record_viewer'):
            context['post_list'] = Post.objects.filter(Q(author=self.request.user) | Q(published='1'))
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'view/detail_new.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.content)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        current = Post.objects.get(pk=self.kwargs.get('pk'))
        post_id = self.kwargs.get('pk')
        form = CommentForm(
            request.POST,
            user=request.user,
            post_id=post_id
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('focus:detail', kwargs={'pk': post_id})
            )

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PostDetailView, self).dispatch(request, *args, **kwargs)


class ArchivesView(ListView):
    model = Post
    template_name = 'view/index_new.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(pub_date__year=year,
                                                               pub_date__month=month
                                                               )

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ArchivesView, self).dispatch(request, *args, **kwargs)


class CategoryView(ListView):
    model = Post
    template_name = 'view/index_new.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        if is_viewer(self.request.user, 'record_viewer'):
            return super(CategoryView, self).get_queryset().filter(category=cate)
        else:
            return super(CategoryView, self).get_queryset().filter(Q(category=cate),
                                                                   Q(author=self.request.user) | Q(published='1'))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryView, self).dispatch(request, *args, **kwargs)


class TagView(ListView):
    model = Post
    template_name = 'view/index_new.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        if is_viewer(self.request.user, 'record_viewer'):
            return super(TagView, self).get_queryset().filter(tags=tag)
        else:
            return super(TagView, self).get_queryset().filter(Q(tags=tag),
                                                              Q(author=self.request.user) | Q(published='1'))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TagView, self).dispatch(request, *args, **kwargs)


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('focus:index'))
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login_new.html', {'form': form})
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid = True
        if not username or not password:
            valid = False
            messages.add_message(request, messages.INFO, 'Username and password cannot be empty')
        user = User.objects.filter(username=username).first()
        if not user:
            valid = False
            messages.add_message(request, messages.INFO, 'User does not exist')
        user = authenticate(username=username, password=password)
        if (user is not None) and valid:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('focus:index'))
            else:
                valid = False
                messages.add_message(request, messages.INFO, 'User deactivated')
        else:
            valid = False
            messages.add_message(request, messages.INFO, 'Incorrect password')
        if not valid:
            return HttpResponseRedirect(reverse('focus:login'))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('focus:login'))


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            t = form.save(commit=False)
            t.author = request.user
            t.save()
        return HttpResponseRedirect(reverse('focus:detail', kwargs={'pk': t.pk}))
    else:
        form = PostForm()

    return render(request, 'create_post_new.html', {'form': form, 'title': 'Create Post'})


@login_required
def edit_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.published:
        return HttpResponseForbidden('Editing is not allowed when post has been published')
    if not post.author == request.user:
        return HttpResponseForbidden('You are not allowed to edit other\'s post')
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            t = form.save()
            return HttpResponseRedirect(reverse('focus:detail', kwargs={'pk': t.pk}))
    else:
        form = PostEditForm(instance=post)

    return render(request, 'edit_post_new.html', {'form': form, 'title': 'Edit Post'})


@login_required
def user_info(request, pk):
    u = User.objects.get(pk=pk)
    if is_viewer(u, 'record_viewer'):
        return render(request, 'user_info.html', {
            'title': u.username,
            'user': u,
            'posts': u.post_set.select_related('category')[:10],
            'comments': u.comment_set.select_related('post', 'user').order_by('-pub_date')[:10],
        })
    else:
        return render(request, 'user_info_new.html', {
            'title': u.username,
            'user': u,
            'posts': u.post_set.filter(Q(published='1') | Q(author=request.user)).select_related('category')[:10],
            'comments': u.comment_set.select_related('post', 'user').order_by('-pub_date')[:10],
        })


class UserTopics(ListView):
    model = Comment
    template_name = 'user_posts_new.html'
    template_name = 'user_posts_new.html'
    template_name = 'user_posts_new.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        if is_viewer(self.request.user, 'record_viewer'):
            return Post.objects.filter(
                author_id=self.kwargs.get('pk')
            ).select_related(
                'author', 'category'
            )
        else:
            return Post.objects.filter(
                Q(author_id=self.kwargs.get('pk')) & (Q(published='1') | (Q(author=self.request.user)))
            ).select_related(
                'author', 'category'
            )

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(pk=self.kwargs.get('pk'))
        context['panel_title'] = context['title'] = context['user'].username
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserTopics, self).dispatch(request, *args, **kwargs)


@login_required
def test(request):
    # This view is missing all form handling logic for simplicity of the example
    return render(request, 'test.html', {'form': StepOneForm()})


class SheetWizard(SessionWizardView):
    template_name = "test.html"
    instance = None

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SheetWizard, self).dispatch(request, *args, **kwargs)

    def get_form_instance(self, step):
        if self.instance is None:
            self.instance = Post()
        return self.instance

    def done(self, form_list, **kwargs):
        self.instance.author = self.request.user
        self.instance.save()
        form_data_dict = self.get_all_cleaned_data()
        tags = form_data_dict.pop('tags')

        for something in tags:
            self.instance.tags.add(something)

        return HttpResponseRedirect(reverse('focus:detail', kwargs={'pk': self.instance.pk}))


def is_viewer(user, group_name):
    try:
        if Group.objects.get(user=user).name == group_name:
            return True
        else:
            return False
    except Group.DoesNotExist:
        return False
