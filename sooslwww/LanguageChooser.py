from django.conf import settings
from django.template import RequestContext, loader
from django.template import Context, loader, RequestContext


def CurrentLanguageID(request):
   return request.session.get( 'language', getattr(settings, 'DEFAULT_LANGUAGE'))

def SetCurrentLanguage(request, language_id):
   request.session['language'] = language_id
