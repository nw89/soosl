from django.core.urlresolvers import reverse

from sooslwww.models import BodyLocation, Gloss, Sentence, Sign, Tag

def AddAttributeUrl(sign, attribute):
    if attribute.__class__ == BodyLocation:
        view = 'sooslwww.views.add_body_location'
    elif attribute.__class__ == Gloss:
        view = 'sooslwww.views.add_gloss'
    elif attribute.__class__ == Tag:
        view = 'sooslwww.views.add_tag'

    return reverse(view,
                   args=(sign.id, attribute.id))

def RemoveAttributeUrl(sign, attribute):
    if attribute.__class__ == BodyLocation:
        view = 'sooslwww.views.remove_body_location'
    elif attribute.__class__ == Gloss:
        view = 'sooslwww.views.remove_gloss'
    elif attribute.__class__ == Tag:
        view = 'sooslwww.views.remove_tag'

    return reverse(view,
                   args=(sign.id, attribute.id))


def ViewSignsWithAttributeUrl(attribute):
    if attribute.__class__ == BodyLocation:
        filter_string = '/body_locations/'
    elif attribute.__class__ == Gloss:
        filter_string = '/glosses/'
    if attribute.__class__ == Tag:
        filter_string = '/tags/'

    filter_string += str(attribute.id)

    return reverse('sooslwww.views.all_signs_filter',
                   kwargs={'filter_string': filter_string})

def SignFilterUrl(filter_string):
    if filter_string == '':
        return reverse('sooslwww.views.all_signs')
    else:
        return reverse('sooslwww.views.all_signs_filter',
                   kwargs={'filter_string': filter_string})

def SentenceAddSignFilterUrl(sentence, filter_string):
    if filter_string == '':
        return reverse('sooslwww.views.sentence_all_signs',
                        kwargs={'sentence_id': sentence.id})
    else:
        return reverse('sooslwww.views.sentence_all_signs_filter',
                   kwargs={'sentence_id': sentence.id,
                           'filter_string': filter_string})


def ViewVideoUrl(video):
    if video.__class__ == Sign:
        return reverse('sooslwww.views.sign',
                       kwargs={'sign_id': video.id})
    elif video.__class__ == Sentence:
        return reverse('sooslwww.views.sentence',
                       kwargs={'sentence_id': video.id})
    else:
        return NotImplementedError
