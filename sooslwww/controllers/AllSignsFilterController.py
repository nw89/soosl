from django.core.urlresolvers import reverse

from sooslwww.models import Tag

from sooslwww.filter.UrlBasedSignFilter import UrlBasedSignFilter

class AllSignsFilterController:
    def __init__(self, filter_string):
	self.url_filter =  UrlBasedSignFilter(filter_string)
	self.filtered_signs = self.url_filter.ObtainFilteredSigns()


    def GetFilteredSigns(self):
	return self.filtered_signs

    def AddTags(self, tag_renderer):
	tags = self._GetRelevantTags()

	for tag in tags:
	    tag_url = reverse(
		'sooslwww.views.all_signs_filter',
		kwargs={'filter_string':
			self.url_filter.ObtainTagFilterString(tag)})

	    tag_renderer.AddTag(
		tag,
		self.url_filter.TagInFilter(tag),
		tag_url)

    def _GetRelevantTags(self):
	'''Returns all the tags that are contained in the\
	filtered signs'''
	return Tag.objects.filter(
	    sign__in=self.GetFilteredSigns()
	    ).distinct().order_by('id')
