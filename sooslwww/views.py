# Create your views here.
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader

from sooslwww.models import Sign

def index(request):
    return HttpResponse("Hello, world. You're at the poll index.")

def sign(request, sign_id):
    requested_sign = get_object_or_404(Sign, id=sign_id);

    t = loader.get_template('sign.html')
    c = Context({
            'sign_id': sign_id,
            })
    return HttpResponse(t.render(c))
