# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from docker_status import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^refresh/$', views.refresh, name='refresh'),
    url(r'^check/(?P<id>.*?)/$', views.check, name='check'),
    url(r'^update/(?P<id>.*?)/$', views.update, name='update'),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
