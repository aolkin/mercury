from django.conf.urls import patterns, url

from . import views

urlpatterns = (
    url('^$', views.index),
    url('^competition/(\d+)/$', views.default),
    url('^competition/(\d+)/compete/$', views.compete),
    url('^competition/(\d+)/judge/$', views.judge),
    url('^competition/(\d+)/admin/$', views.admin),
    url('^scoreboard/(\d+)/$', views.scoreboard),
    url('^scoreboard/$', views.scoreboard),
)
