from django.conf.urls import url
from . import views
from .forms import StepOneForm, StepTwoForm, StepThreeForm

app_name = 'focus'
urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^home/$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.login_view, name='login'),
    url(r'^page/(?P<page>[0-9]+)/$', views.IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^category/(?P<pk>[0-9]+)/page/(?P<page>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^tag/(?P<pk>[0-9]+)/page/(?P<page>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    url(r'^u/(?P<pk>\d+)/$', views.user_info, name='user_info'),
    url(r'^u/(?P<pk>\d+)/topics/page/(?P<page>[0-9]+)/$', views.UserTopics.as_view(), name='user_posts'),
    url(r'^u/(?P<pk>\d+)/topics/$', views.UserTopics.as_view(), name='user_posts'),
    url(r'^post/create/$', views.SheetWizard.as_view([StepOneForm, StepTwoForm, StepThreeForm]), name='create_post'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.edit_post, name='edit_post'),
    # url(r'^search/$', views.search, name='search'),
    url(r'^test/$', views.SheetWizard.as_view([StepOneForm, StepTwoForm, StepThreeForm]), name='test'),
]
