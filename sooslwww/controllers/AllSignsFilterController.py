from django.shortcuts import render_to_response
from django.template import RequestContext
from sooslwww.LanguageChooser import CurrentLanguageID
from sooslwww.controllers.Controller import AbstractController
from sooslwww.filter.UrlBasedSignFilter import UrlBasedSignFilter
from sooslwww.models import BodyLocation, Gloss, Tag
from sooslwww.renderers import AttributeRenderer, BodyLocationRenderer
from sooslwww.urlresolver import SignFilterUrl, SentenceAddSignFilterUrl


class AllSignsFilterController(AbstractController):
    def __init__(self, filter_string):
        AbstractController.__init__(self)

        self._url_filter = UrlBasedSignFilter(filter_string)

        self._tag_renderer = AttributeRenderer()
        self._gloss_renderer = AttributeRenderer()
        self._body_location_renderer = BodyLocationRenderer()

    def _PreprocessRequest(self, request):
        self._language_ID = CurrentLanguageID(request)

        self.AddAttributes(Tag)
        self.AddAttributes(Gloss)
        self.AddAttributes(BodyLocation)

        self._AddToDictionary('all_signs',
                              self._url_filter.ObtainFilteredSigns())

        tag_text = self._tag_renderer.Render(request,
                                             'tags.html',
                                             'tags')

        self._AddToDictionary('tag_text', tag_text)


        gloss_text = self._gloss_renderer.Render(request,
                                                 'gloss_list.html',
                                                 'glosses')

        self._AddToDictionary('gloss_text', gloss_text)

        body_location_text = self._body_location_renderer.Render(
            request,
            'svg/body_locations.svg')

        self._AddToDictionary('body_location_text',
                              body_location_text)


    def AddAttributes(self, attribute_type):
        attributes = self._GetRelevantAttributes(attribute_type)

        for attribute in attributes:
            url = self._GetUrlFromToggleString(
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
        '''Returns all the attributes are contained in the\
        filtered signs'''
        relevant_attributes = attribute_type.objects.filter(
            sign__in=self._url_filter.ObtainFilteredSigns()
            ).distinct().order_by('id')

        if attribute_type == Gloss:
            #Remove all that aren't the current language
            relevant_attributes = [gloss for gloss in \
                                   relevant_attributes if \
                                   (gloss.language.id == \
                                   self._language_ID)]

        return relevant_attributes

    def _TemplateFile(self):
        return 'all_signs.html'

    def _GetUrlFromToggleString(self, toggle_string):
        return SignFilterUrl(toggle_string)

class SentenceAllSignsFilterController(AllSignsFilterController):
    def __init__(self, sentence, filter_string):
        AllSignsFilterController.__init__(self, filter_string)
        self._sentence = sentence
        self._AddToDictionary('sentence', sentence)

    def _TemplateFile(self):
        return 'sentence_all_signs.html'

    def _GetUrlFromToggleString(self, toggle_string):
        return SentenceAddSignFilterUrl(self._sentence,
                                        toggle_string)
