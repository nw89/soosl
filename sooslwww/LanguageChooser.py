from django.conf import settings
from django.template import RequestContext, loader
from django.template import Context, loader, RequestContext

from sooslwww.models import WrittenLanguage


def DefaultLanguageID(request):
   return request.session.get( 'language', getattr(settings, 'DEFAULT_LANGUAGE'))

def SetDefaultLanguage(request, language_id):
   request.session['language'] = language_id
