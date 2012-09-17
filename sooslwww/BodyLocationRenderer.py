from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from sooslwww.models import BodyHeadLocationType, BodyLocation

class BodyLocationWithAttributes:
    def __init__(self, selected, url, body_location):
        self._selected = selected
        self._url = url
        self._body_location = body_location

    def Selected(self):
        return self._selected

    def Url(self):
        return self._url

    def GetBodyLocationShape(self):
        return self._body_location.get_instance()

class BodyLocationRenderer:
    def __init__(self):
        self._locations = list()

    def AddLocation(self, selected, url, location):
        self._locations.append(
            BodyLocationWithAttributes(selected, url, location))

    def Render(self, request, render_head):
        behind_locations_str = ''
        in_front_locations_str = ''

        for location in self._locations:
            shape = location.GetBodyLocationShape()
            location_string = loader.render_to_string(
                "svg/" + shape.Shape_str() + ".svg",
                {"location_type": shape.type.text,
                 "selected" : location.Selected(),
                 "shape": shape,
                 "url": location.Url() })
            if shape.behind:
                behind_locations_str += location_string
            else:
                in_front_locations_str += location_string

        location_types = BodyHeadLocationType.objects.all()

        return loader.render_to_string(
            "svg/body_locations.svg",
            {"location_types": location_types,
             "show_head": render_head,
             "behind_body_locations": behind_locations_str,
             "in_front_body_locations": in_front_locations_str},
            context_instance=RequestContext(request))

def GetSVGForSign(sign, edit, request):
    at_least_one_head_location = sign.HasAHeadLocation()
    if at_least_one_head_location:
        body_locations = BodyLocation.objects.all()
    else:
        body_locations = BodyLocation.objects.filter(
            on_head=False)

    body_location_renderer = BodyLocationRenderer()

    for location in body_locations:

        if sign.HasBodyLocation(location):
            location_url = reverse(
                'sooslwww.views.remove_body_location',
                args=(sign.id,
                      location.id))
        else:
            location_url = reverse(
                'sooslwww.views.add_body_location',
                args=(sign.id,
                      location.id))

        body_location_renderer.AddLocation(
            sign.HasBodyLocation(location),
            location_url,
            location)

    return body_location_renderer.Render(request,
                                         at_least_one_head_location)
