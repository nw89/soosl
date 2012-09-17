import re

from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from sooslwww.BodyLocationRenderer import BodyLocationRenderer
from sooslwww.filter.UrlBasedSignFilter import UrlBasedSignFilter
from sooslwww.models import BodyLocation, Gloss, Tag
from sooslwww.renderers import GlossRenderer, TagRenderer


class AllSignsFilterController:
    def __init__(self, filter_string):

        p = re.compile('(?:/tags/(?P<tag_string>(?:\d+,)*\d+))?(?:/glosses/(?P<gloss_string>(?:\d+,)*\d+))?(?:/body_locations/(?P<body_location_string>(?:\d+,)*\d+))?')

        matches = p.match(filter_string)

        if matches == None:
            raise Http404

        tag_string = matches.group('tag_string')
        gloss_string = matches.group('gloss_string')
        body_location_string = matches.group('body_location_string')

        self.url_filter = UrlBasedSignFilter(
            tag_string,
            gloss_string,
            body_location_string)

        self._tag_renderer = TagRenderer()
        self._gloss_renderer = GlossRenderer()

    def Render(self, request):
        self.AddTags()
        self.AddGlosses()

        return render_to_response(
        'all_signs.html',
        {'all_signs': self.url_filter.ObtainFilteredSigns(),
         'tag_text': self._tag_renderer.Render(request),
         'gloss_text': self._gloss_renderer.Render(
                    request, 'gloss_list.html'),
         'url_prefix': request.path},
        context_instance=RequestContext(request)
        )

    def RenderBodyLocations(self, request):
        renderer = BodyLocationRenderer()

        locations = self._GetRelevantBodyLocations()

        for location in locations:
            location_url = self._ObtainLocationUrl(location) + \
                '/body_locations.svg'
                 #Must add this as the svg lives in its own frame

            renderer.AddLocation(
                self.url_filter.BodyLocationInFilter(location),
                location_url,
                location)

        return renderer.Render( request, True)

    def AddTags(self):
        tags = self._GetRelevantTags()

        for tag in tags:
            tag_url = self._ObtainTagUrl(tag)

            self._tag_renderer.AddTag(
                tag,
                self.url_filter.TagInFilter(tag),
                tag_url)

    def AddGlosses(self):
        glosses = self._GetRelevantGlosses()

        for gloss in glosses:
            gloss_url = self._ObtainGlossUrl(gloss)

            self._gloss_renderer.AddGloss(
                gloss,
                self.url_filter.GlossInFilter(gloss),
                gloss_url)

    def _ObtainTagUrl(self, tag):
        tag_string = self.url_filter.ObtainTagFilterString(tag)
        gloss_string = self.url_filter.ObtainAllGlossesString()
        body_location_string = self.url_filter.ObtainAllBodyLocationsString()

        return self._ObtainUrl(tag_string,
                               gloss_string,
                               body_location_string)

    def _ObtainGlossUrl(self, gloss):
        tag_string = self.url_filter.ObtainAllTagsString()
        gloss_string = self.url_filter.ObtainGlossFilterString(gloss)
        body_location_string = self.url_filter.ObtainAllBodyLocationsString()

        return self._ObtainUrl(tag_string,
                               gloss_string,
                               body_location_string)


    def _ObtainLocationUrl(self, location):
        tag_string = self.url_filter.ObtainAllTagsString()
        gloss_string = self.url_filter.ObtainAllGlossesString()
        body_location_string = self.url_filter.\
            ObtainBodyLocationFilterString(location)

        return self._ObtainUrl(tag_string,
                               gloss_string,
                               body_location_string)

    def _ObtainUrl(self, tag_string, gloss_string, body_location_string):
        filter_string = ''

        if tag_string != '':
            filter_string += '/tags/' + tag_string

        if gloss_string != '':
            filter_string += '/glosses/' + gloss_string

        if body_location_string != '':
            filter_string += '/body_locations/' + body_location_string

        if filter_string == '':
            url = reverse('sooslwww.views.all_signs')
        else:
            url = reverse(
                'sooslwww.views.all_signs_filter',
                kwargs={'filter_string': filter_string})

        return url

    def _GetRelevantTags(self):
        '''Returns all the tags that are contained in the\
        filtered signs'''
        return Tag.objects.filter(
            sign__in=self.url_filter.ObtainFilteredSigns()
            ).distinct().order_by('id')


    def _GetRelevantGlosses(self):
        '''Returns all the glosses that are contained in the\
        filtered signs'''
        return Gloss.objects.filter(
            sign__in=self.url_filter.ObtainFilteredSigns()
            ).distinct().order_by('id')

    def _GetRelevantBodyLocations(self):
        '''Returns all the body locations that are contained in the\
        filtered signs'''
        return BodyLocation.objects.filter(
            sign__in=self.url_filter.ObtainFilteredSigns()
            ).distinct().order_by('id')
