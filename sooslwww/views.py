from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext

from sooslwww.forms import AddSignForm
from sooslwww.models import Gloss, Sign, Tag, WrittenLanguage, BodyLocation

from sooslwww.LanguageChooser import SetCurrentLanguage
from sooslwww.videoHandler import VideoUploadHandler

from sooslwww.controllers.AllSignsFilterController import AllSignsFilterController
from sooslwww.controllers.SignController import SignControllerView, SignControllerEdit

from sooslwww.BodyLocationRenderer import GetSVGForSign, BodyLocationRenderer

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


def sign(request, sign_id, edit=False):
    if edit:
        controller = SignControllerEdit(sign_id)
    else:
        controller = SignControllerView(sign_id)

    return controller.Render(request, edit)

def edit_sign(request, sign_id):
    return sign(request, sign_id, True)

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
        reverse('sooslwww.views.body_location_view',
                args=(requested_sign.id,)
                ))


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
    if request.method == 'POST':
        form = AddSignForm(request.POST, request.FILES)
        if form.is_valid():
            uploadedVideo = request.FILES['videoFile'];

            videoHandler = VideoUploadHandler(uploadedVideo)

            #Check to see if the video has been updated already
            if Sign.objects.filter(videohash=videoHandler.hash()):
                errors = form._errors.setdefault(
                    "videoFile", ErrorList())
                errors.append("That video has already been uploaded.")

            else:
                #Proceed to save it
                success = videoHandler.encodeVideo()

                if not success:
                    errors = form._errors.setdefault(
                    "videoFile", ErrorList())
                    errors.append("That video could not be converted.")
                else:
                    newsign = Sign(videohash=videoHandler.hash())
                    newsign.save()
                    return HttpResponseRedirect(
                        reverse('sooslwww.views.sign', args=(newsign.id,))
                        )


    else:
        form = AddSignForm()
    return render_to_response(
        'addsign.html',
        {'form': form},
        context_instance=RequestContext(request)
        )

def body_location_view(request, sign_id):
    return body_location(request, sign_id, False)

def body_location_edit(request, sign_id):
    return body_location(request, sign_id, True)

def body_location(request, sign_id, edit):
    requested_sign = get_object_or_404(Sign, id=sign_id)

    svg = GetSVGForSign(requested_sign, edit, request)

    response = HttpResponse(mimetype = "image/svg+xml")
    response.write(svg)
    return response

def body_location_all(request):
    return body_location_filter(request, '')

def body_location_filter(request, filter_string):
    controller = AllSignsFilterController(filter_string)
    svg = controller.RenderBodyLocations(request)

    response = HttpResponse(mimetype = "image/svg+xml")
    response.write(svg)
    return response;

def select_language(request, language_id):
    if not WrittenLanguage.objects.filter(id=language_id).exists():
        raise Http404

    SetCurrentLanguage(request, language_id)
    return HttpResponseRedirect(request.path[0:-18])


def thumbnail(request, sign_id):
    requested_sign = get_object_or_404(Sign, id=sign_id)

    filePath = "%s/videos/thumbnails/%s.gif" % (
        getattr(settings, 'MEDIA_ROOT'), requested_sign.videohash)

    return utils.generateFileHttpResponse(filePath, "image/gif");

def video(request, sign_id):
    requested_sign = get_object_or_404(Sign, id=sign_id)

    filePath = "%s/videos/mp4/%s.mp4" % (
        getattr(settings, 'MEDIA_ROOT'), requested_sign.videohash)

    return utils.generateFileHttpResponse(filePath, "video/mp4");
