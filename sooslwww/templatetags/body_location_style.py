from django.template import Library

register = Library()

from sooslwww.models import BodyHeadLocationType

def body_location_style():
    location_types = BodyHeadLocationType.objects.all()

    return {'location_types': location_types}

register.inclusion_tag('body_location_style.html', takes_context=False)(body_location_style)
