from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url('^$', views.index),
    url('^vote/([a-z0-9]+)/$', views.vote),
    url('^manage/([a-z0-9]+)/$', views.manage),
    url('^manage/([a-z0-9]+)/results/$', views.get_results),
    url('^new/$', views.new),
)
