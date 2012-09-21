from django.shortcuts import get_object_or_404
from sooslwww.controllers.Controller import AbstractController
from sooslwww.models import Sentence
from sooslwww.renderers import AttributeRenderer
from sooslwww.urlresolver import ViewVideoUrl


class SentenceController(AbstractController):
    def __init__(self, sentence_id):
        AbstractController.__init__(self)
        self._requested_sentence = get_object_or_404(Sentence,
                             id=sentence_id)

    def _PreprocessRequest(self, request):
        self.__AddSignText(request)

        self._AddToDictionary('sentence',
                              self._requested_sentence)

    def __AddSignText(self, request):
        sign_renderer = AttributeRenderer()

        signs = self._GetRelevantSigns()

        for sign in signs:
            sign_renderer.AddAttribute(
                sign,
                self._GetSignUrl(sign),
                False)

        sign_text = sign_renderer.Render(request,
                                         self._SignsTemplateFile(),
                                         'signs')

        self._AddToDictionary('sign_text', sign_text)

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

    def _GetRelevantSigns(self):
        return self._requested_sentence.GetSigns()

    def _GetSignUrl(self, sign):
        raise NotImplementedError

    def _TemplateFile(self):
        raise NotImplementedError

class SentenceControllerView(SentenceController):
    def __init__(self, sentence_id):
        SentenceController.__init__(self, sentence_id)

    def _GetSignUrl(self, sign):
        return ViewVideoUrl(sign)

    def _TemplateFile(self):
        return 'sentence/sentence_view.html'

    def _SignsTemplateFile(self):
        return 'sentence/signs.html'

class SentenceControllerEdit(SentenceController):
    def __init__(self, sentence_id):
        SentenceController.__init__(self, sentence_id)

    def _GetSignUrl(self, sign):
        return ViewVideoUrl(sign)

    def _TemplateFile(self):
        return 'sentence/sentence_edit.html'

    def _SignsTemplateFile(self):
        return 'sentence/signs_edit.html'
