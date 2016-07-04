# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView


blog_urls = ([
    url(r'^zinnia/', include('zinnia.urls.capabilities')),
    url(r'^search/', include('zinnia.urls.search')),
    url(r'^sitemap/', include('zinnia.urls.sitemap')),
    url(r'^trackback/', include('zinnia.urls.trackback')),
    url(r'^writing/tags/', include('zinnia.urls.tags')),
    url(r'^writing/feeds/', include('zinnia.urls.feeds')),
    url(r'^writing/random/', include('zinnia.urls.random')),
    url(r'^writing/authors/', include('zinnia.urls.authors')),
    url(r'^writing/categories/', include('zinnia.urls.categories')),
    url(r'^writing/comments/', include('zinnia.urls.comments')),
    url(r'^writing/', include('zinnia.urls.entries')),
    url(r'^writing/', include('zinnia.urls.archives')),
    url(r'^writing/', include('zinnia.urls.shortlink')),
    url(r'^writing/', include('zinnia.urls.quick_entry'))
], 'zinnia')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),
    url(r'^', include(blog_urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
