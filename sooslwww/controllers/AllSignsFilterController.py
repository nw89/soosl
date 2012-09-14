from django.core.urlresolvers import reverse

from sooslwww.models import Tag

from sooslwww.filter.UrlBasedSignFilter import UrlBasedSignFilter

class AllSignsFilterController:
    def __init__(self, tag_string, gloss_string):
	self.url_filter =  UrlBasedSignFilter(
	    tag_string,
	    gloss_string)
	self.filtered_signs = self.url_filter.ObtainFilteredSigns()

    def GetFilteredSigns(self):
	return self.filtered_signs

    def AddTags(self, tag_renderer):
	tags = self._GetRelevantTags()

	for tag in tags:
	    tag_url = self._ObtainTagUrl(tag)

	    tag_renderer.AddTag(
		tag,
		self.url_filter.TagInFilter(tag),
		tag_url)

    def _ObtainTagUrl(self, tag):
	tag_string = self.url_filter.ObtainTagFilterString(tag)
	gloss_string = self.url_filter.ObtainAllGlossesString()

	if (tag_string == '' and gloss_string == ''):
	    return reverse('sooslwww.views.all_signs')

	elif tag_string == '':
	    return reverse(
		'sooslwww.views.all_signs_filter_gloss',
		kwargs={'gloss_string': gloss_string})

	elif gloss_string == '':
	    return reverse(
		'sooslwww.views.all_signs_filter_tag',
		kwargs={'tag_string': tag_string})
	else:
	    return reverse( 'sooslwww.views.\all_signs_filter_tag_gloss',
			    kwargs={'tag_string': tag_string,
				    'gloss_string': gloss_string})

    def _GetRelevantTags(self):
	'''Returns all the tags that are contained in the\
	filtered signs'''
	return Tag.objects.filter(
	    sign__in=self.GetFilteredSigns()
	    ).distinct().order_by('id')
