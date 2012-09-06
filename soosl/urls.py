
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sooslwww/$', 'sooslwww.views.all_signs'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/$', 'sooslwww.views.sign'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/edit$', 'sooslwww.views.edit_sign'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/add_tag/(?P<tag_id>\d+)$', 'sooslwww.views.add_tag'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/remove_tag/(?P<tag_id>\d+)$', 'sooslwww.views.remove_tag'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/thumbnail.gif$',
        'sooslwww.views.thumbnail'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/video.mp4$',
        'sooslwww.views.video'),
    url(r'^sooslwww/add_sign/$', 'sooslwww.views.add_sign'),
    url(r'^sooslwww/all_signs/$', 'sooslwww.views.all_signs'),
    url(r'^sooslwww/all_signs/filter/(?P<filter_string>(?:\d+,)*(?:\d+)?)$', 'sooslwww.views.all_signs_filter'),
    url(r'^admin/', include(admin.site.urls)),
)
