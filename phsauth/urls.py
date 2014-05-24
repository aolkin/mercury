from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url('^login/', views.login_page, name="login"),
    url('^logout/', views.logout_page, name="logout"),
#    url('^password/', views.change_password, name="change_password"),
)
