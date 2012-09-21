from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import  RequestContext


class RedirectingException(Exception):
    def __init__(self, url):
        self.url = url

class AbstractController(object):
    def __init__(self):
        self._dictionary = {}

    def Render(self, request):
        try:
            self._PreprocessRequest(request)
        except RedirectingException, e:
            return HttpResponseRedirect(e.url)

        return render_to_response(
            self._TemplateFile(),
            self._dictionary,
            context_instance=RequestContext(request))

    def _AddToDictionary(self, key, value):
        self._dictionary[key] = value

    def _PreprocessRequest(self, request):
        raise NotImplementedError

    def _TemplateFile(self):
        raise NotImplementedError
