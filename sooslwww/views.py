from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from sooslwww.LanguageChooser import SetCurrentLanguage
from sooslwww.controllers.AddVideoController import AddSignController, AddSentenceController
from sooslwww.controllers.AllSignsFilterController import AllSignsFilterController, SentenceAllSignsFilterController
from sooslwww.controllers.SentenceController import SentenceControllerView, SentenceControllerEdit
from sooslwww.controllers.SignController import SignControllerView, SignControllerEdit
from sooslwww.models import Gloss, Sentence, Sign, Tag, WrittenLanguage, BodyLocation

import utils


def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def importBP(request):
    from sooslwww.ImportBodyParts import ImportBodyParts
    ImportBodyParts()
    return HttpResponse("Import finished")

def all_body_locations(request):
    renderer = BodyLocationRenderer()
    all_locations = BodyLocation.objects.all()
    for location in all_locations:
        renderer.AddLocation(False, 'test', location)
    svg = renderer.Render(request)
    response = HttpResponse(mimetype = "image/svg+xml")
    response.write(svg)
    return response


def sign(request, sign_id):
    controller = SignControllerView(sign_id)

    return controller.Render(request)

def edit_sign(request, sign_id):
    controller = SignControllerEdit(sign_id)
    return controller.Render(request)

def sentence(request, sentence_id):
    controller = SentenceControllerView(sentence_id)
    return controller.Render(request)

def sentence_edit(request, sentence_id):
    controller = SentenceControllerEdit(sentence_id)
    return controller.Render(request)

def add_tag(request, sign_id, tag_id):
    return add_remove_tag(request, sign_id, tag_id, False)

def remove_tag(request, sign_id, tag_id):
    return add_remove_tag(request, sign_id, tag_id, True)

def add_remove_tag(request, sign_id, tag_id, remove_tag):
    requested_sign = get_object_or_404(Sign, id=sign_id)
    tag = get_object_or_404(Tag, id=tag_id)

    if remove_tag:
        requested_sign.tags.remove(tag)
    else:
        requested_sign.tags.add(tag)

    return HttpResponseRedirect(
        reverse('sooslwww.views.edit_sign', args=(requested_sign.id,))
        )

def add_body_location(request, sign_id, body_location_id):
    return add_remove_body_location(request,
                                    sign_id,
                                    body_location_id,
                                    False)

def remove_body_location(request,
                         sign_id,
                         body_location_id):
    return add_remove_body_location(request,
                                    sign_id,
                                    body_location_id,
                                    True)

def add_remove_body_location(request,
                             sign_id,
                             body_location_id,
                             remove_body_location):
    requested_sign = get_object_or_404(Sign, id=sign_id)
    body_location = get_object_or_404(BodyLocation,
                                      id=body_location_id)

    if remove_body_location:
        requested_sign.RemoveBodyLocation(body_location)
    else:
        requested_sign.AddBodyLocation(body_location)

    return HttpResponseRedirect(
        reverse('sooslwww.views.edit_sign', args=(requested_sign.id,))
        )


def remove_gloss(request, sign_id, gloss_id):
    gloss = get_object_or_404(Gloss, id=gloss_id)
    sign = get_object_or_404(Sign, id=sign_id)

    sign.glosses.remove(gloss)
    return HttpResponseRedirect(
        reverse('sooslwww.views.edit_sign', args=(sign.id,))
        )

def all_signs(request):
    return all_signs_filter(request, '')

def all_signs_filter(request, filter_string):
    controller = AllSignsFilterController(filter_string)
    return controller.Render(request)

def add_sign(request):
    controller = AddSignController()
    return controller.Render(request)

def add_sentence(request):
    controller = AddSentenceController()
    return controller.Render(request)

def body_location_all(request):
    return body_location_filter(request, '')

def body_location_filter(request, filter_string):
    controller = AllSignsFilterController(filter_string)
    svg = controller.RenderBodyLocations(request)

    response = HttpResponse(mimetype = "image/svg+xml")
    response.write(svg)
    return response;

def select_language(request, language_id):
    if not WrittenLanguage.objects.filter(id=int(language_id)).exists():
        raise Http404

    SetCurrentLanguage(request, int(language_id))
    return HttpResponseRedirect(request.path[0:-18])


def sign_thumbnail(request, sign_id):
    requested_sign = get_object_or_404(Sign, id=sign_id)

    filePath = "%s/videos/thumbnails/%s.gif" % (
        getattr(settings, 'MEDIA_ROOT'), requested_sign.videohash)

    return utils.generateFileHttpResponse(filePath, "image/gif");


def sentence_video(request, sentence_id):
    requested_sentence = get_object_or_404(Sentence, id=sentence_id)

    filePath = "%s/videos/mp4/%s.mp4" % (
        getattr(settings, 'MEDIA_ROOT'), requested_sentence.videohash)

    return utils.generateFileHttpResponse(filePath, "video/mp4");

def sign_video(request, sign_id):
    requested_sign = get_object_or_404(Sign, id=sign_id)

    filePath = "%s/videos/mp4/%s.mp4" % (
        getattr(settings, 'MEDIA_ROOT'), requested_sign.videohash)

    return utils.generateFileHttpResponse(filePath, "video/mp4")

def sentence_thumbnail(request, sentence_id):
    requested_sentence = get_object_or_404(Sentence, id=sentence_id)

    filePath = "%s/videos/thumbnails/%s.gif" % (
        getattr(settings, 'MEDIA_ROOT'), requested_sentence.videohash)

    return utils.generateFileHttpResponse(filePath, "image/gif")

def sentence_all_signs(request, sentence_id):
    return sentence_all_signs_filter(request, sentence_id, '')

def sentence_all_signs_filter(request, sentence_id, filter_string):
    requested_sentence = get_object_or_404(Sentence, id=sentence_id)
    controller = SentenceAllSignsFilterController(
        requested_sentence,
        filter_string)
    return controller.Render(request)

def sentence_add_sign(request, sentence_id, sign_id):
    return sentence_add_remove_sign(request,
                           sentence_id,
                           sign_id,
                           False)

def sentence_remove_sign(request, sentence_id, sign_id):
    return sentence_add_remove_sign(request,
                           sentence_id,
                           sign_id,
                           True)

def sentence_add_remove_sign(request,
                             sentence_id,
                             sign_id,
                             remove_sign):
    requested_sentence = get_object_or_404(Sentence,
                                           id=sentence_id)

    sign = get_object_or_404(Sign,
                             id=sign_id)

    if remove_sign:
        requested_sentence.signs.remove(sign)
    else:
        requested_sentence.signs.add(sign)

    return HttpResponseRedirect(
        reverse('sooslwww.views.sentence_edit'
                , args=(requested_sentence.id,))
        )

def body_location_all(request):
    return body_location_filter(request, '')

def body_location_filter(request, filter_string):
    controller = AllSignsFilterController(filter_string)
    svg = controller.RenderBodyLocations(request)

    response = HttpResponse(mimetype = "image/svg+xml")
    response.write(svg)
    return response;

def select_language(request, language_id):
    if not WrittenLanguage.objects.filter(id=int(language_id)).exists():
        raise Http404

    SetCurrentLanguage(request, int(language_id))
    return HttpResponseRedirect(request.path[0:-18])


def thumbnail(request, sign_id):
    requested_sign = get_object_or_404(Sign, id=sign_id)

    filePath = "%s/videos/thumbnails/%s.gif" % (
        getattr(settings, 'MEDIA_ROOT'), requested_sign.videohash)

    return utils.generateFileHttpResponse(filePath, "image/gif");
