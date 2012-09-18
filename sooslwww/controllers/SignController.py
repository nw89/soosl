from django.shortcuts import render_to_response, get_object_or_404
from django.template import  RequestContext
from sooslwww.urlresolver import AddAttributeUrl, RemoveAttributeUrl, ViewSignsWithAttributeUrl

from sooslwww.LanguageChooser import CurrentLanguageID
from sooslwww.forms import AddGlossForm
from sooslwww.models import Sign, Tag
from sooslwww.renderers import GlossRenderer, TagRenderer
from sooslwww.utils import AddNewGloss


class SignController(object):
    def __init__(self, sign_id):
        self._requested_sign = get_object_or_404(Sign, id=sign_id);

    def Render(self, request, edit):
        self._PreprocessRequest(request)

        return render_to_response(
            self.TemplateFile(),
            dict(
                {'sign': self._requested_sign,
                 'tag_text': self.GetTagText(request),
                 'gloss_text': self._GetGlossText(request),
                 }.items() +
                self._GetExtraComponents().items()),
            context_instance=RequestContext(request))

    def GetTagText(self,request):
        tag_renderer = TagRenderer()

        tags = self._GetRelevantTags()

        for tag in tags:
            tag_renderer.AddTag(
                tag,
                self._AttributeIsSelected(tag),
                self._GetAttributeUrl(tag)
                )

        return tag_renderer.Render(request)

    def _GetRelevantTags(self):
        raise NotImplementedError

    def _GetGlossText(self, request):
        glosses = self._requested_sign.glosses.filter(
            language__id=CurrentLanguageID(request))

        gloss_renderer = GlossRenderer()
        for gloss in glosses:
            # A gloss isn't ever selected when viewing a sign
            gloss_renderer.AddGloss(gloss,
                                    False,
                                    self._GetAttributeUrl(gloss))

        return gloss_renderer.Render(
            request,
            self._GlossTemplateFile())

    def _GetExtraComponents(self):
        return {}

    def _PreprocessRequest(self, request):
        pass

    def _GlossTemplateFile(self):
        return 'gloss_list.html'

    def _AttributeIsSelected(self, attribute):
        raise NotImplementedError

    def _GetAttributeUrl(self, attribute):
        raise NotImplementedError


class SignControllerEdit(SignController):
    def __init__(self, sign_id):
        super(SignControllerEdit, self).__init__(sign_id)

    def TemplateFile(self):
        return 'sign/sign_edit.html'

    def _AttributeIsSelected(self, attribute):
        return self._requested_sign.HasAttribute(attribute)

    def _GetAttributeUrl(self, attribute):
        if self._AttributeIsSelected(attribute):
            url =  RemoveAttributeUrl(self._requested_sign,
                                     attribute)
        else:
            url =  AddAttributeUrl(self._requested_sign,
                                      attribute)

        return url

    def _GlossTemplateFile(self):
        return 'sign/sign_glosses_edit.html'

    def EditMode(self):
        return True

    def _GetExtraComponents(self):
        return {'add_gloss_form': self._ObtainGlossForm()}

    def _GetRelevantTags(self):
        # Return all available tags
        return Tag.objects.all()

    def _PreprocessRequest(self, request):
        if request.method == 'POST':
            self._add_gloss_form = AddGlossForm(request.POST)
            if self._add_gloss_form.is_valid():
                AddNewGloss(
                    self._requested_sign,
                    CurrentLanguageID(request),
                    self._add_gloss_form.cleaned_data['gloss_text'])

                #Clear form
                self._add_gloss_form = AddGlossForm()

        else:
            self._add_gloss_form = AddGlossForm()

    def _ObtainGlossForm(self):
        return self._add_gloss_form


class SignControllerView(SignController):
    def __init__(self, sign_id):
        super(SignControllerView, self).__init__(sign_id)

    def TemplateFile(self):
        return 'sign/sign_view.html'

    def _AttributeIsSelected(self, attribute):
        # When viewing a sign, an attribute is never selected
        return False;

    def _GetAttributeUrl(self, attribute):
        return ViewSignsWithAttributeUrl(attribute)

    def EditMode(self):
        return False

    def _GetRelevantTags(self):
        #Return only tags the sign has
        return self._requested_sign.tags.all()
