import string

from sooslwww.models import Sign, Tag
import utils

class UrlBasedSignFilter:
    def __init__(self, filter_string):
	self.tag_strings = self._ExtractTags(filter_string)

    def ObtainFilteredSigns(self):
	# TODO: In production use a query

	# Start with all signs
	filtered_signs = list(Sign.objects.all())

	# Remove based on every tag
	for tag_string in self.tag_strings:
	    filtered_signs = [sign for sign in filtered_signs \
				  if sign.HasTag(tag_string)]

	return filtered_signs

    def TagInFilter(self, tag):
	return (self.tag_strings.count(str(tag.id)) > 0)

    def ObtainTagFilterString(self, tag):
	#Copy the tag_strings
	tag_strings_copy = list(self.tag_strings)

	tag_string = str(tag.id)

	if self.TagInFilter(tag):
	    # Remove it from the tag strings
	    tag_strings_copy.remove(tag_string)
	else:
	    # Append it to the tag strings
	    tag_strings_copy.append(tag_string)

	new_filter_string = self._GenerateNewTagFilterString(
	    tag_strings_copy)

	return new_filter_string

    def _ExtractTags(self, filter_string):
	if filter_string == '':
	    tag_strings = []
	else:
	    tag_strings = string.split(filter_string, ',')
	return tag_strings

    def _GenerateNewTagFilterString(self,tag_strings):
	new_tag_filter_string = ''

	for tag_string in tag_strings:
	    new_tag_filter_string += tag_string + ','

	return (utils.StripLastComma(new_tag_filter_string))
