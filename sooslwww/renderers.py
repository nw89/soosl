from django.template import RequestContext, loader

class RenderedAttribute(object):
    def __init__(self, text, url, selected):
        self.text = text
        self.selected = selected
        self.url = url

class Renderer(object):
    def __init__(self):
        self._attributes = []

    def Render(self, request):
        raise NotImplementedError


    def _AddAttribute(self, attributes):
        self._attributes.append(attributes)

    def _RenderTemplate(self, request, template, attribute_name):
           return loader.render_to_string(
             template,
             {attribute_name: self._attributes},
             context_instance=RequestContext(request))


class RenderedTag(RenderedAttribute):
    def __init__(self, tag, url, selected):
        RenderedAttribute.__init__(self, tag.text, url, selected)
        self.graphic = tag.graphic
        assert(self.text == tag.text)

class TagRenderer(Renderer):
    def AddTag(self, tag, selected, tag_url):
        self._AddAttribute(
            RenderedTag(tag, tag_url, selected)
            )

    def Render(self, request):
        return self._RenderTemplate(request, 'tags.html', 'tags')

class GlossRenderer(Renderer):
    def AddGloss(self, gloss, selected, url):
        self._AddAttribute(
            RenderedAttribute(gloss.text, url, selected))

    def Render(self, request, template):
        return self._RenderTemplate(
            request,
            template,
            'glosses')
