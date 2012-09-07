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
