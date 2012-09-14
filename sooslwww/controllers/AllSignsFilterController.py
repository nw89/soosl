from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from sooslwww.models import Gloss, Tag

from sooslwww.filter.UrlBasedSignFilter import UrlBasedSignFilter
from sooslwww.renderers import GlossRenderer, TagRenderer


class AllSignsFilterController:
    def __init__(self, tag_string, gloss_string):
        self.url_filter =  UrlBasedSignFilter(
            tag_string,
            gloss_string)

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
                    request, 'gloss_list.html')
         },
        context_instance=RequestContext(request)
        )


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

        return self._ObtainUrl(tag_string, gloss_string)

    def _ObtainGlossUrl(self, gloss):
        tag_string = self.url_filter.ObtainAllTagsString()
        gloss_string = self.url_filter.ObtainGlossFilterString(gloss)

        return self._ObtainUrl(tag_string, gloss_string)


    def _ObtainUrl(self, tag_string, gloss_string):
        if (tag_string == '' and gloss_string == ''):
            url = reverse('sooslwww.views.all_signs')

        elif tag_string == '':
            url = reverse(
                'sooslwww.views.all_signs_filter_gloss',
                kwargs={'gloss_string': gloss_string})

        elif gloss_string == '':
            url = reverse(
                'sooslwww.views.all_signs_filter_tag',
                kwargs={'tag_string': tag_string})
        else:
            url = reverse( 'sooslwww.views.all_signs_filter',
                            kwargs={'tag_string': tag_string,
                                    'gloss_string': gloss_string})
        return url

    def _GetRelevantTags(self):
        '''Returns all the tags that are contained in the\
        filtered signs'''
        return Tag.objects.filter(
            sign__in=self.url_filter.ObtainFilteredSigns()
            ).distinct().order_by('id')


    def _GetRelevantGlosses(self):
        '''Returns all the tags that are contained in the\
        filtered signs'''
        return Gloss.objects.filter(
            sign__in=self.url_filter.ObtainFilteredSigns()
            ).distinct().order_by('id')
