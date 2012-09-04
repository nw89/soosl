# Create your views here.
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

from sooslwww.forms import AddSignForm
from sooslwww.models import Sign

from sooslwww.utils import encode_video

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def sign(request, sign_id):
    requested_sign = get_object_or_404(Sign, id=sign_id);

    t = loader.get_template('sign.html')
    c = Context({
            'sign_id': sign_id,
            })
    return HttpResponse(t.render(c))

def add_sign(request):
    if request.method == 'POST':
        form = AddSignForm(request.POST, request.FILES)
        if form.is_valid():

            newsign = Sign(videopath=request.FILES['videoFile'])
            newsign.save()

            encode_video(request.FILES['videoFile']);

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
