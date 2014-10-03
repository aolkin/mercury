from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

from django.conf import settings

from config import uncached_config

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url=uncached_config.get("main_url","/admin/config/config/main_url/"),permanent=False)),

    url(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL+"favicon.ico")),

    url(r'^voting/', include('voting.urls')),
    url(r'^competingcode/', include('codecompetitions.urls')),

    url(r'^user/', include('phsauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
