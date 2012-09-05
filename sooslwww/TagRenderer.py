from django.template import RequestContext, loader

class SelectableTag():
    def __init__(self, id, text, graphic, tag_class, tag_url):
        self.id = id
        self.text = text
        self.graphic = graphic
        self.tag_class = tag_class
        self.tag_url = tag_url

class TagRenderer:
    def __init__(self):
        self._tags = []

    def AddTag(self, id, text, graphic, tag_class, tag_url):
        new_tag = SelectableTag(id,
                                text,
                                graphic,
                                tag_class,
                                tag_url)
        self._tags.append(new_tag)


    def Render(self, request):

        return loader.render_to_string('tags.html',
                                       {'tags': self._tags
                                        },
                                       context_instance=RequestContext(request))
