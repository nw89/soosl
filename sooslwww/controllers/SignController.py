from django.shortcuts import get_object_or_404

from sooslwww.LanguageChooser import CurrentLanguageID
from sooslwww.controllers.Controller import AbstractController
from sooslwww.forms import AddGlossForm
from sooslwww.models import Sign, BodyLocation, Tag
from sooslwww.renderers import AttributeRenderer, BodyLocationRenderer
from sooslwww.urlresolver import AddAttributeUrl, RemoveAttributeUrl, ViewSignsWithAttributeUrl, ViewVideoUrl
from sooslwww.utils import AddNewGloss


class SignController(AbstractController):
    def __init__(self, sign_id):
        AbstractController.__init__(self)
        self._requested_sign = get_object_or_404(Sign, id=sign_id)

    def _PreprocessRequest(self, request):
        self._AddToDictionary('sign', self._requested_sign)

        self.__AddBodyLocationText(request)
        self.__AddTagText(request)
        self.__AddGlossText(request)
        self.__AddSentenceText(request)

    def __AddTagText(self, request):
        tag_renderer = AttributeRenderer()

        tags = self._GetRelevantTags()

        for tag in tags:
            tag_renderer.AddAttribute(
                tag,
                self._GetAttributeUrl(tag),
                self._TagIsSelected(tag),
                )

        tag_text = tag_renderer.Render(request, 'tags.html', 'tags')

        self._AddToDictionary('tag_text', tag_text)

    def _GetRelevantTags(self):
        raise NotImplementedError

    def _TagIsSelected(self, attribute):
        raise NotImplementedError

    def __AddGlossText(self, request):
        gloss_renderer = AttributeRenderer()

        glosses = self._requested_sign.\
            GlossesForLanguage(CurrentLanguageID(request))

        for gloss in glosses:
            gloss_renderer.AddAttribute(
            gloss,
            self._GetAttributeUrl(gloss),
            self._GlossIsSelected(gloss))

        gloss_text =  gloss_renderer.Render(request,
                            'gloss_list.html',
                            'glosses')

        self._AddToDictionary('gloss_text', gloss_text)

    def __AddSentenceText(self, request):
        sentence_renderer = AttributeRenderer()

        sentences = self._GetRelevantSentences()

        for sentence in sentences:
            sentence_renderer.AddAttribute(
                sentence,
                self._GetSentenceUrl(sentence),
                False)

        sentence_text = sentence_renderer.Render(request,
                                         self._SentencesTemplateFile(),
                                         'sentences')

        self._AddToDictionary('sentence_text', sentence_text)


    def __AddBodyLocationText(self, request):
        if self._requested_sign.HasAHeadLocation():
            body_locations = BodyLocation.objects.all()
        else:
            body_locations = BodyLocation.objects.filter(
            on_head=False)

        body_location_renderer = BodyLocationRenderer()

        for location in body_locations:
            body_location_renderer.AddAttribute(
            location,
            self._GetAttributeUrl(location),
            self._BodyLocationIsSelected(location))

        body_locations_text = body_location_renderer.Render(
            request,
            'body_locations.svg')

        self._AddToDictionary('body_locations_text',
                      body_locations_text)

    def _BodyLocationIsSelected(self, location):
        return self._requested_sign.HasBodyLocation(location)

    def _GetRelevantSentences(self):
        return self._requested_sign.GetSentences()

    def _GetSentenceUrl(self, sentence):
        return ViewVideoUrl(sentence)

    def _SentencesTemplateFile(self):
        return 'sign/sentences.html'

    def _GetAttributeUrl(self, attribute):
        raise NotImplementedError

class SignControllerEdit(SignController):
    def __init__(self, sign_id):
        SignController.__init__(self, sign_id)

    def _PreprocessRequest(self, request):
        if request.method == 'POST':
            add_gloss_form = AddGlossForm(request.POST)
            if add_gloss_form.is_valid():
                AddNewGloss(
                    self._requested_sign,
                    CurrentLanguageID(request),
                    add_gloss_form.cleaned_data['gloss_text'])

            #Clear form
            add_gloss_form = AddGlossForm()

        else:
            add_gloss_form = AddGlossForm()

        #Add the gloss form
        self._AddToDictionary('add_gloss_form',
                      add_gloss_form)

        #Call parent method to finish the job
        SignController._PreprocessRequest(self, request)

    def _TemplateFile(self):
        return 'sign/sign_edit.html'

    def _TagIsSelected(self, attribute):
        return self._requested_sign.HasAttribute(attribute)

    def _GlossIsSelected(self, attribute):
        # When editing ka sign, a gloss is always selected
        return True

    def _GetAttributeUrl(self, attribute):
        if self._TagIsSelected(attribute):
            url =  RemoveAttributeUrl(self._requested_sign,
                                      attribute)
        else:
            url =  AddAttributeUrl(self._requested_sign,
                                   attribute)

            return url

    def _GlossTemplateFile(self):
        return 'sign/sign_glosses_edit.html'

    def _GetRelevantTags(self):
        # Return all available tags
        return Tag.objects.all()

class SignControllerView(SignController):
    def __init__(self, sign_id):
        SignController.__init__(self, sign_id)

    def _TemplateFile(self):
        return 'sign/sign_view.html'

    def _GetAttributeUrl(self, attribute):
        return ViewSignsWithAttributeUrl(attribute)

    def _TagIsSelected(self, attribute):
        # When viewing a sign, a tag is never selected
        return False

    def _GlossIsSelected(self, attribute):
        # When viewing a sign, a gloss is never selected
        return False

    def _GetRelevantTags(self):
        #Return only tags the sign has
        return self._requested_sign.tags.all()
