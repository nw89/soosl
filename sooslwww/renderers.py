from django.template import RequestContext, loader

from sooslwww.models import WrittenLanguage, Gloss

from sooslwww.LanguageChooser import CurrentLanguageID

class GlossRenderer:
    def RenderSign(self, request, sign, edit_mode=False):
        glosses = sign.glosses.filter(
            language__id=CurrentLanguageID(request))

        return loader.render_to_string(
            'sign_glosses.html',
            {'glosses': glosses,
             'sign': sign,
             'edit_mode': edit_mode
             },
            context_instance=RequestContext(request))


class RenderedTag():
    def __init__(self, tag, selected, tag_url):
        self.text = tag.text
        self.graphic = tag.graphic
        self.selected = selected
        self.tag_url = tag_url

class TagRenderer:
    def __init__(self):
        self._tags = []

    def AddTag(self, tag, selected, tag_url):
        self._tags.append(
            RenderedTag(tag, selected, tag_url)
            )

    def Render(self, request):
        return loader.render_to_string(
            'tags.html',
            {'tags': self._tags},
            context_instance=RequestContext(request))
