from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sooslwww/$', 'sooslwww.views.index'),
    url(r'^sooslwww/(?P<sign_id>\d+)/$', 'sooslwww.views.sign'),
    url(r'^sooslwww/add_sign/$', 'sooslwww.views.add_sign'),
    url(r'^admin/', include(admin.site.urls)),
)
