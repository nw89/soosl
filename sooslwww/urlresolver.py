from django.core.urlresolvers import reverse

from sooslwww.models import BodyLocation, Gloss, Tag

def AddAttributeUrl(sign, attribute):
    if type(attribute) == BodyLocation:
        view = 'sooslwww.views.add_body_location'
    elif type(attribute) == Gloss:
        view = 'sooslwww.views.add_gloss'
    elif type(attribute) == Tag:
        view = 'sooslwww.views.add_tag'

    return reverse(view,
                   args=(sign.id, attribute.id))

def RemoveAttributeUrl(sign, attribute):
    if type(attribute) == BodyLocation:
        view = 'sooslwww.views.remove_body_location'
    elif type(attribute) == Gloss:
        view = 'sooslwww.views.remove_gloss'
    elif type(attribute) == Tag:
        view = 'sooslwww.views.remove_tag'

    return reverse(view,
                   args=(sign.id, attribute.id))


def ViewSignsWithAttributeUrl(attribute):
    if type(attribute) == BodyLocation:
        filter_string = '/body_locations/'
    elif type(attribute) == Gloss:
        filter_string = '/glosses/'
    if type(attribute) == Tag:
        filter_string = '/tags/'

    filter_string += str(attribute.id)

    return reverse('sooslwww.views.all_signs_filter',
                   kwargs={'filter_string': filter_string})
