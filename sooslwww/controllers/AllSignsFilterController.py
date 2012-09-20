from django.shortcuts import render_to_response
from django.template import RequestContext

from sooslwww.filter.UrlBasedSignFilter import UrlBasedSignFilter
from sooslwww.models import BodyLocation, Gloss, Tag
from sooslwww.renderers import AttributeRenderer, BodyLocationRenderer
from sooslwww.urlresolver import SignFilterUrl

class AllSignsFilterController:
    def __init__(self, filter_string):
        self._url_filter = UrlBasedSignFilter(filter_string)

        self._tag_renderer = AttributeRenderer()
        self._gloss_renderer = AttributeRenderer()
        self._body_location_renderer = BodyLocationRenderer()

    def Render(self, request):
        self.AddAttributes(Tag)
        self.AddAttributes(Gloss)
        self.AddAttributes(BodyLocation)

        return render_to_response(
        'all_signs.html',
        {'all_signs': self._url_filter.ObtainFilteredSigns(),
         'tag_text': self._tag_renderer.Render(request,
                                               'tags.html',
                                               'tags'),
         'gloss_text': self._gloss_renderer.Render(request,
                                                   'gloss_list.html',
                                                   'glosses'),
         'body_location_text': self._body_location_renderer.\
             Render(request,
                    'svg/body_locations.svg',
                    'body_locations'),
         'url_prefix': request.path},
        context_instance=RequestContext(request)
        )

    def AddAttributes(self, attribute_type):
        attributes = self._GetRelevantAttributes(attribute_type)

        for attribute in attributes:
            url = SignFilterUrl(
                self._url_filter.ObtainToggleFilterString(attribute))

            self._GetRenderer(attribute_type).AddAttribute(
                attribute,
                url,
                self._url_filter.InFilter(attribute)
                )

    def _GetRenderer(self, attribute_type):
        if attribute_type == BodyLocation:
            return self._body_location_renderer
        if attribute_type == Gloss:
            return self._gloss_renderer
        elif attribute_type == Tag:
            return self._tag_renderer
        else:
            raise NotImplemented

    def _GetRelevantAttributes(self, attribute_type):
        '''Returns all the attribtues are contained in the\
        filtered signs'''
        return attribute_type.objects.filter(
            sign__in=self._url_filter.ObtainFilteredSigns()
            ).distinct().order_by('id')
