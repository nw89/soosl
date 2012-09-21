from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                         url(r'^$', 'sooslwww.views.all_signs'),
                       # url(r'^import$', 'sooslwww.views.importBP'),
                         url(r'^all_body_locations$', 'sooslwww.views.all_body_locations'),
                         url(r'^sign/(?P<sign_id>\d+)/$', 'sooslwww.views.sign'),
                         url(r'^sign/(?P<sign_id>\d+)/edit/$', 'sooslwww.views.edit_sign'),
                         url(r'^sign/(?P<sign_id>\d+)/add_tag/(?P<tag_id>\d+)$', 'sooslwww.views.add_tag'),
                         url(r'^sign/(?P<sign_id>\d+)/remove_tag/(?P<tag_id>\d+)$', 'sooslwww.views.remove_tag'),
                         url(r'^sign/(?P<sign_id>\d+)/add_body_location/(?P<body_location_id>\d+)$', 'sooslwww.views.add_body_location'),
                         url(r'^sign/(?P<sign_id>\d+)/remove_body_location/(?P<body_location_id>\d+)$', 'sooslwww.views.remove_body_location'),
                         url(r'^sign/(?P<sign_id>\d+)/remove_gloss/(?P<gloss_id>\d+)$', 'sooslwww.views.remove_gloss'),
                         url(r'^sign/(?P<sign_id>\d+)/thumbnail\.gif$', 'sooslwww.views.sign_thumbnail'),
                         url(r'^sign/(?P<sign_id>\d+)/video.mp4$', 'sooslwww.views.sign_video'),
                         url(r'^sentence/(?P<sentence_id>\d+)/$', 'sooslwww.views.sentence'),
                         url(r'^sentence/(?P<sentence_id>\d+)/edit$', 'sooslwww.views.sentence_edit'),
                         url(r'^sentence/(?P<sentence_id>\d+)/thumbnail\.gif$','sooslwww.views.sentence_thumbnail'),
                         url(r'^sentence/(?P<sentence_id>\d+)/video.mp4$',
                           'sooslwww.views.sentence_video'),
                         url(r'^add_sign$', 'sooslwww.views.add_sign'),
                         url(r'^add_sentence$', 'sooslwww.views.add_sentence'),
                         url(r'^all_signs$', 'sooslwww.views.all_signs'),
                         url(r'^all_signs/body_locations.svg$', 'sooslwww.views.body_location_all'),
                         url(r'(?:.*)/select_language/(?P<language_id>\d+$)', 'sooslwww.views.select_language'),
                         url(r'^all_signs/filter(?P<filter_string>(?:/\w+/(?:\d+,)*\d+)+)$', 'sooslwww.views.all_signs_filter'),
                         url(r'^all_signs/filter(?P<filter_string>(?:/\w+/(?:\d+,)*\d+)+)/body_locations.svg$', 'sooslwww.views.body_location_filter'),
                         url(r'^admin/', include(admin.site.urls)),
                         url(r'^sentence/(?P<sentence_id>\d+)/add/filter$', 'sooslwww.views.sentence_all_signs'),
                         url(r'^sentence/(?P<sentence_id>\d+)/add/filter(?P<filter_string>(?:/\w+/(?:\d+,)*\d+)+)$', 'sooslwww.views.sentence_all_signs_filter'),
                        url(r'^sentence/(?P<sentence_id>\d+)/add/(?P<sign_id>\d+)$', 'sooslwww.views.sentence_add_sign'),
                        url(r'^sentence/(?P<sentence_id>\d+)/remove/(?P<sign_id>\d+)$', 'sooslwww.views.sentence_remove_sign')
                       )
