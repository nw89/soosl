from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.forms.util import ErrorList
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

from sooslwww.forms import AddSignForm
from sooslwww.models import Gloss, Sign, Tag, WrittenLanguage
from sooslwww.utils import AddNewGloss

from sooslwww.LanguageChooser import SetCurrentLanguage, CurrentLanguageID
from sooslwww.GlossRenderer import GlossRenderer
from sooslwww.TagRenderer import TagRenderer
from sooslwww.videoHandler import VideoUploadHandler

from sooslwww.controllers.AllSignsFilterController import AllSignsFilterController
from sooslwww.controllers.SignController import SignControllerView, SignControllerEdit

import string
import utils

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

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

# def add_gloss(request, sign_id):
#     if request.method

def remove_gloss(request, sign_id, gloss_id):
    gloss = get_object_or_404(Gloss, id=gloss_id)
    sign = get_object_or_404(Sign, id=sign_id)

    sign.glosses.remove(gloss)
    return HttpResponseRedirect(
	reverse('sooslwww.views.edit_sign', args=(sign.id,))
	)



def all_signs(request):
    return all_signs_filter(request, '', '')

def all_signs_filter_tag(request, tag_string):
    return all_signs_filter(request, tag_string, '')

def all_signs_filter_gloss(request, tag_string):
    return all_signs_filter(request, tag_string, '')

def all_signs_filter(request, tag_string, gloss_string):
    controller = AllSignsFilterController(tag_string, gloss_string)

    filtered_signs = controller.GetFilteredSigns();

    tag_renderer = TagRenderer()
    controller.AddTags(tag_renderer)

    tag_text = tag_renderer.Render(request)

    return render_to_response(
	'all_signs.html',
	{'all_signs': filtered_signs,
	 'tag_text': tag_text},
	context_instance=RequestContext(request)
	)

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
