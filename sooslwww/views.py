from django.conf import settings
from django.core.urlresolvers import resolve, reverse
from django.forms.util import ErrorList
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

from sooslwww.forms import AddSignForm, AddGlossForm
from sooslwww.models import Gloss, Sign, Tag, WrittenLanguage
from sooslwww.utils import AddNewGloss

from sooslwww.LanguageChooser import SetCurrentLanguage, CurrentLanguageID
from sooslwww.GlossRenderer import GlossRenderer
from sooslwww.TagRenderer import TagRenderer
from sooslwww.videoHandler import VideoUploadHandler


import string
import utils

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def sign(request, sign_id, edit=False):
    requested_sign = get_object_or_404(Sign, id=sign_id);

    tagRenderer = TagRenderer()


    if edit:
        #Load all tags
        all_tags = Tag.objects.all()

        for tag in all_tags:
            signs_matching_tag = requested_sign.tags.filter(id=tag.id);
            if signs_matching_tag.exists():
                tag_class = 'selected_edit_tag'
                tag_url = reverse('sooslwww.views.remove_tag',
                                  args=(requested_sign.id,
                                        tag.id))

            else:
                tag_class = 'edit_tag'
                tag_url = reverse('sooslwww.views.add_tag',
                                  args=(requested_sign.id,
                                        tag.id))

            tagRenderer.AddTag(tag.id, tag.text, tag.graphic, tag_class, tag_url)

        # Handle gloss form
        if request.method == 'POST':
            add_gloss_form = AddGlossForm(request.POST)
            if add_gloss_form.is_valid():
                AddNewGloss(requested_sign,
                            CurrentLanguageID(request),
                            add_gloss_form.cleaned_data['gloss_text'])

                #Clear form
                add_gloss_form = AddGlossForm()

        else:
            add_gloss_form = AddGlossForm()


    else:
        #Just sign tags
        sign_tags = requested_sign.tags.all()

        for tag in sign_tags:
            tagRenderer.AddTag(tag.id, tag.text, tag.graphic, 'normal_tag', '')

    tagText = tagRenderer.Render(request)

    print tagText

    glossRenderer = GlossRenderer()
    glossText = glossRenderer.RenderSign(request, requested_sign, edit)

    if edit:
        return render_to_response(
            'sign.html',
            {'sign': requested_sign,
             'tag_text': tagText,
             'gloss_text': glossText,
             'edit_mode': True,
             'add_gloss_form': add_gloss_form},
            context_instance=RequestContext(request))
    else:
        return render_to_response(
            'sign.html',
            {'sign': requested_sign,
             'tag_text': tagText,
             'gloss_text': glossText,
             'edit_mode': False},
            context_instance=RequestContext(request))

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
    return all_signs_filter(request, '')

def all_signs_filter(request, filter_string):
    if filter_string != '':
        #Extract tags
        tag_strings = string.split(filter_string, ',')
    else:
        tag_strings = []

    #Start will all signs and filter by each tag
    filtered_signs = list(Sign.objects.all())

    for tag_string in tag_strings:
        for filtered_sign in filtered_signs:
            has_tag = (filtered_sign.tags.filter(id__exact=tag_string)).exists()
            if not has_tag:
                filtered_signs.remove(filtered_sign)

    #TODO: In production use a question query

    #Render the tags
    tagRenderer = TagRenderer()

    #Load all relevant tags
    # all_tags = Tag.objects.all()
    all_tags = Tag.objects.filter(sign__in=filtered_signs).distinct().order_by('id')

    for tag in all_tags:
        tag_in_filter = (tag_strings.count(str(tag.id)) > 0)

        if tag_in_filter:
            tag_class = 'selected_edit_tag'
            tags_string_without_tag = ''
            for tag_string in tag_strings:
                if tag_string != str(tag.id):
                    tags_string_without_tag += tag_string + ','

            # Remove last comma
            new_filter_string = tags_string_without_tag[:-1]

        else:
            tag_class = 'edit_tag'
            if filter_string == '':
                new_filter_string = str(tag.id)
            else:
                new_filter_string = filter_string + ',' + str(tag.id)

        tag_url  = reverse('sooslwww.views.all_signs_filter',
                           kwargs={'filter_string': new_filter_string})



        tagRenderer.AddTag(tag.id, tag.text, tag.graphic, tag_class, tag_url)

    tagText = tagRenderer.Render(request)

    return render_to_response(
        'all_signs.html',
        {'all_signs': filtered_signs,
         'tag_text': tagText},
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
