from django.template import RequestContext, loader

class RenderedAttribute(object):
    def __init__(self, attribute, url, selected):
        self.model = attribute
        self.selected = selected
        self.url = url

class AttributeRenderer(object):
    def __init__(self):
        self._attributes = []

    def AddAttribute(self, attribute, url, selected):
        self._attributes.append(
            RenderedAttribute(attribute, url, selected)
            )

    def Render(self, request, template, attribute_name):
        return loader.render_to_string(
            template,
            {attribute_name: self._attributes},
            context_instance=RequestContext(request))

class BodyLocationRenderer(AttributeRenderer):
    def __init__(self):
        AttributeRenderer.__init__(self)
        self._behind_locations_string = ''
        self._in_front_locations_string = ''
        self._render_head = False

    def Render(self, request, template):
        for location in self._attributes:
            self._RenderLocation(location)

        return loader.render_to_string(
            "svg/body_locations.svg",
            {"show_head": self._render_head,
             "behind_body_locations": self._behind_locations_string,
             "in_front_body_locations": self._in_front_locations_string},
            context_instance=RequestContext(request))

    def _RenderLocation(self, location):
        shape = location.model.get_instance()

        location_string = loader.render_to_string(
            "svg/" + shape.Shape_str() + ".svg",
            {"location_type": shape.type.text,
             "selected" : location.selected,
             "shape": shape,
             "url": location.url })

        if shape.behind:
            self._behind_locations_string += location_string
        else:
            self._in_front_locations_string += location_string

        if shape.on_head:
             self._render_head = True
