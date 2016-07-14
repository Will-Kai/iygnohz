# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.conf.urls import url
from django.views.static import serve
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ]
