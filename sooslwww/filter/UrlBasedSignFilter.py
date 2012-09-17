import string

from sooslwww.filter.filters import MultiFilter
from sooslwww.models import Gloss, Sign, Tag
from sooslwww import utils

class InvalidTagException(Exception):
    pass

def ExtractTags(filter_string):
    if filter_string == '' or filter_string == None:
        tag_strings = []
    else:
        tag_strings = string.split(filter_string, ',')
    return tag_strings

def CreateCommaSeparatedString(string_list):
    filter_string = ''

    for s in string_list:
        filter_string += s + ','

    return(utils.StripLastComma(filter_string))


class StringList:
    def __init__(self, string_list):
        self._string_list = string_list

    def Strings(self):
        return self._string_list

    def InList(self, string):
        return (self._string_list.count(string) > 0)

    def CommaSeparatedString(self):
        return (CreateCommaSeparatedString
                (self._string_list))

    def CreateCSStringExcluding(self, string):
        string_list_copy = list(self._string_list)
        string_list_copy.remove(string)
        return(CreateCommaSeparatedString
               (string_list_copy))

    def CreateCSStringIncluding(self, string):
        string_list_copy = list(self._string_list)
        string_list_copy.append(string)
        return(CreateCommaSeparatedString
               (string_list_copy))


class UrlBasedSignFilter:
    def __init__(self,
                 tag_string,
                 gloss_string,
                 body_location_string):
        self._tag_strings = StringList(ExtractTags(tag_string))
        self._gloss_strings = StringList(ExtractTags(gloss_string))
        self._body_location_strings = StringList(
            ExtractTags(body_location_string))

        self._multi_filter = MultiFilter()

        # TODO: In production use a query
        self._AddFilters(self._tag_strings, Tag)
        self._AddFilters(self._gloss_strings, Gloss)

        # Start with all signs
        self._filtered_signs = self._multi_filter.FilterSigns(
            list(Sign.objects.all()))

    def ObtainFilteredSigns(self):
        return self._filtered_signs

    def TagInFilter(self, tag):
        return self._tag_strings.InList(str(tag.id))

    def GlossInFilter(self, gloss):
        return self._gloss_strings.InList(str(gloss.id))

    def BodyLocationInFilter(self, body_location):
        return self._body_location_strings.InList(
            str(body_location.id))

    def ObtainTagFilterString(self, tag):
        if self.TagInFilter(tag):
            tag_string = self._tag_strings.\
                CreateCSStringExcluding(str(tag.id))
        else:
            tag_string = self._tag_strings.\
                CreateCSStringIncluding(str(tag.id))

        return tag_string

    def ObtainAllTagsString(self):
        return (self._tag_strings.CommaSeparatedString())

    def ObtainGlossFilterString(self, gloss):
        if self.GlossInFilter(gloss):
            gloss_string = self._gloss_strings.\
                CreateCSStringExcluding(str(gloss.id))
        else:
            gloss_string = self._gloss_strings.\
                CreateCSStringIncluding(str(gloss.id))

        return gloss_string

    def ObtainAllGlossesString(self):
        return (self._gloss_strings.CommaSeparatedString())

    def ObtainBodyLocationFilterString(self, body_location):
        if self.BodyLocationInFilter(body_location):
            body_location_string = self._body_location_strings.\
                CreateCSStringExcluding(str(body_location.id))
        else:
            body_location_string = self._body_location_strings.\
                CreateCSStringIncluding(str(body_location.id))

        return body_location_string

    def ObtainAllBodyLocationsString(self):
        return (self._body_location_strings.CommaSeparatedString())


    def _AddFilters(self, string_list, type):
        for string in string_list.Strings():
            attribute = type.objects.get(id=int(string))
            self._multi_filter.AddFilter(attribute)
