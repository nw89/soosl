from django.shortcuts import render_to_response, get_object_or_404
from django.template import  RequestContext
from django.core.urlresolvers import reverse

from sooslwww.GlossRenderer import GlossRenderer
from sooslwww.LanguageChooser import CurrentLanguageID
from sooslwww.TagRenderer import TagRenderer

from sooslwww.forms import AddGlossForm
from sooslwww.models import Sign, Tag

from sooslwww.utils import AddNewGloss


class SignController(object):
    def __init__(self, sign_id):
	self._requested_sign = get_object_or_404(Sign, id=sign_id);
	self._tag_renderer = TagRenderer()
	self._gloss_renderer = GlossRenderer()

    def Render(self, request, edit):
	glossText = self._gloss_renderer.RenderSign(request, self._requested_sign, self.EditMode())

	return render_to_response(
	    self.TemplateFile(),
	    dict(
		{'sign': self._requested_sign,
		 'tag_text': self.GetTagText(request),
		 'gloss_text': glossText,
		 }.items() +
		self.GetExtraComponents(request).items()),
	    context_instance=RequestContext(request))

class SignControllerEdit(SignController):
    def __init__(self, sign_id):
	super(SignControllerEdit, self).__init__(sign_id)

    def TemplateFile(self):
	return 'sign/sign_edit.html'

    def EditMode(self):
	return True

    def GetExtraComponents(self, request):
	return {'add_gloss_form': self._ObtainGlossForm(request)}

    def GetTagText(self, request):
	#Load all tags
	all_tags = Tag.objects.all()

	for tag in all_tags:
	    signs_matching_tag = self._requested_sign.tags.filter(id=tag.id);
	    selected = signs_matching_tag.exists()

	    if selected:
		tag_url = reverse('sooslwww.views.remove_tag',
				  args=(self._requested_sign.id,
					tag.id))
	    else:
		tag_url = reverse('sooslwww.views.add_tag',
				  args=(self._requested_sign.id,
					tag.id))

	    self._tag_renderer.AddTag(tag, selected, tag_url)
	return self._tag_renderer.Render(request)

    def _ObtainGlossForm(self, request):
	if request.method == 'POST':
	    add_gloss_form = AddGlossForm(request.POST)
	    if add_gloss_form.is_valid():
		AddNewGloss(self._requested_sign,
			    CurrentLanguageID(request),
			    add_gloss_form.cleaned_data['gloss_text'])

		#Clear form
		add_gloss_form = AddGlossForm()

	else:
	    add_gloss_form = AddGlossForm()

	return add_gloss_form


class SignControllerView(SignController):
    def __init__(self, sign_id):
	super(SignControllerView, self).__init__(sign_id)

    def TemplateFile(self):
	return 'sign/sign_view.html'

    def EditMode(self):
	return False

    def GetExtraComponents(self, request):
	return {}

    def GetTagText(self, request):
	#Just sign tags
	sign_tags = self._requested_sign.tags.all()

	for tag in sign_tags:
	    self._tag_renderer.AddTag(tag, False, '')

	return self._tag_renderer.Render(request)
