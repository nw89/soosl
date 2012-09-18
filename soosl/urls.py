from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'sooslwww.views.all_signs'),
                       #url(r'^import$', 'sooslwww.views.importBP'),
                       url(r'^all_body_locations$', 'sooslwww.views.all_body_locations'),
                       url(r'^sign/(?P<sign_id>\d+)/$', 'sooslwww.views.sign'),
                       url(r'^sign/(?P<sign_id>\d+)/edit/$', 'sooslwww.views.edit_sign'),
                       url(r'^sign/(?P<sign_id>\d+)/add_tag/(?P<tag_id>\d+)$', 'sooslwww.views.add_tag'),
                       url(r'^sign/(?P<sign_id>\d+)/remove_tag/(?P<tag_id>\d+)$', 'sooslwww.views.remove_tag'),
                       url(r'^sign/(?P<sign_id>\d+)/add_body_location/(?P<body_location_id>\d+)$', 'sooslwww.views.add_body_location'),
                       url(r'^sign/(?P<sign_id>\d+)/remove_body_location/(?P<body_location_id>\d+)$', 'sooslwww.views.remove_body_location'),
                       url(r'^sign/(?P<sign_id>\d+)/remove_gloss/(?P<gloss_id>\d+)$', 'sooslwww.views.remove_gloss'),
                       url(r'^sign/(?P<sign_id>\d+)/thumbnail\.gif$',
                           'sooslwww.views.thumbnail'),
                       url(r'^sign/(?P<sign_id>\d+)/body_locations\.svg$',
                           'sooslwww.views.body_location_view'),
                       url(r'^sign/(?P<sign_id>\d+)/body_locations_edit\.svg$',
                           'sooslwww.views.body_location_edit'),
                       url(r'^sign/(?P<sign_id>\d+)/video.mp4$',
                           'sooslwww.views.video'),
                       url(r'^add_sign$', 'sooslwww.views.add_sign'),
                       url(r'^all_signs$', 'sooslwww.views.all_signs'),
                       url(r'^all_signs/body_locations.svg$', 'sooslwww.views.body_location_all'),
                       url(r'^all_signs/filter(?P<filter_string>(?:/\w+/(?:\d+,)*\d+)+)$', 'sooslwww.views.all_signs_filter'),
                       url(r'^all_signs/filter(?P<filter_string>(?:/\w+/(?:\d+,)*\d+)+)/body_locations.svg$', 'sooslwww.views.body_location_filter'),
                       url(r'(?:.*)/select_language/(?P<language_id>\d+$)', 'sooslwww.views.select_language'),
                       url(r'^admin/', include(admin.site.urls)),
                       )
