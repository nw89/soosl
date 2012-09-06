from django.template import RequestContext, loader

from sooslwww.models import WrittenLanguage, Gloss

from sooslwww.LanguageChooser import DefaultLanguageID

class GlossRenderer:
    def RenderSign(self, request, sign):
        glosses = sign.glosses.filter(
            language__id=DefaultLanguageID(request))

        return loader.render_to_string(
            'sign_glosses.html',
            {'glosses': glosses
             },
            context_instance=RequestContext(request))
