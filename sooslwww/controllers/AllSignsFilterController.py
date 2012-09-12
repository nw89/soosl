from django.core.urlresolvers import reverse

from sooslwww.models import Tag

from sooslwww.TagRenderer import TagRenderer
from sooslwww.UrlBasedSignFilter import UrlBasedSignFilter

class AllSignsFilterController:
    def __init__(self, filter_string):
        self.url_filter =  UrlBasedSignFilter(filter_string)
        self.filtered_signs = self.url_filter.ObtainFilteredSigns()

        self.tagRenderer = TagRenderer()

    def GetFilteredSigns(self):
        return self.filtered_signs

    def GetTagText(self, request):
        #Load all relevant tags
        all_tags = Tag.objects.filter(sign__in=self.GetFilteredSigns()).distinct().order_by('id')

        for tag in all_tags:
            if self.url_filter.TagInFilter(tag):
                tag_class = 'selected_edit_tag'

            else:
                tag_class = 'edit_tag'

            new_filter_string = self.url_filter.ObtainTagFilterString(tag)

            tag_url = reverse('sooslwww.views.all_signs_filter',
                              kwargs={'filter_string': new_filter_string})



            self.tagRenderer.AddTag(tag.id, tag.text, tag.graphic, tag_class, tag_url)

        return self.tagRenderer.Render(request)
