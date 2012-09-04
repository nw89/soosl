
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sooslwww/$', 'sooslwww.views.index'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/$', 'sooslwww.views.sign'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/thumbnail.gif$',
	'sooslwww.views.thumbnail'),
    url(r'^sooslwww/sign/(?P<sign_id>\d+)/video.mp4$',
	'sooslwww.views.video'),
    url(r'^sooslwww/add_sign/$', 'sooslwww.views.add_sign'),
    url(r'^admin/', include(admin.site.urls)),
)
