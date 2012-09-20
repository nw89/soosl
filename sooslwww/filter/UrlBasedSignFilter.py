import re, string

from django.http import Http404

from sooslwww import utils
from sooslwww.filter.filters import MultiFilter
from sooslwww.models import BodyLocation, Gloss, Sign, Tag


def CreateCommaSeparatedString(string_list):
    filter_string = ''

    for s in string_list:
        filter_string += s + ','

    return(utils.StripLastComma(filter_string))


class CSVStringProcessor:
    def __init__(self, name, attribute_type, csv_string):
        self._name = name
        self._type = attribute_type
        self._strings = self._ExtractTags(csv_string)

    def Strings(self):
        return self._strings

    def Name(self):
        return self._name

    def Attribute_Type(self):
        return self._type

    def InList(self, attribute_string):
        return (self._strings.count(attribute_string) > 0)

    def Empty(self):
        return (len(self._strings > 0))

    def ObtainCSString(self):
        return self._AppendName(CreateCommaSeparatedString
                                (self._strings))

    def ObtainModifiedCSString(self,
                               attribute_string):

        modified_string = self._CreateModifiedCSString(
            attribute_string)

        modified_string = self._AppendName(modified_string)

        return modified_string

    def _CreateModifiedCSString(self, filter_string):
        exclude_attribute = (self.InList(filter_string))

        string_list_copy = list(self._strings)

        if exclude_attribute:
            string_list_copy.remove(filter_string)
        else:
            string_list_copy.append(filter_string)

        return(CreateCommaSeparatedString
               (string_list_copy))

    def _AppendName(self, filter_string):
        # Only append if not empty
        if filter_string == '':
            return ''
        else:
            return ('/' + self.Name() + '/' + filter_string)

    def _ExtractTags(self, filter_string):
        if filter_string == '' or filter_string == None:
            return []
        else:
            return string.split(filter_string, ',')


class FilterStringProcessor:
    def __init__(self, filter_string, types):
        self._string_processors = list()

        self._ProcessFilterString(filter_string, types)

    def InList(self, attribute):
        for string_processor in self._string_processors:
            if string_processor.Attribute_Type() == attribute.__class__:
                return string_processor.InList(str(attribute.id))

        raise NotImplementedError

    def ObtainAttributes(self):
        attributes = list()

        for string_processor in self._string_processors:
            attribute_strings = string_processor.Strings()
            for attribute_string in attribute_strings:
                attributes.append(
                    string_processor.\
                        Attribute_Type().objects.get(id=attribute_string)
                    )

        return attributes

    def ObtainToggleFilterString(self, attribute):
        filter_string = ''

        for string_list in self._string_processors:
            if string_list.Attribute_Type() == attribute.__class__:
                filter_string += \
                    string_list.ObtainModifiedCSString(
                    str(attribute.id))
            else:
                filter_string += \
                    string_list.ObtainCSString()

        return filter_string

    def _ProcessFilterString(self, filter_string, types):

        url_resolver = re.compile(self._ObtainREString(types))

        matches = url_resolver.match(filter_string)

        self._ProcessMatches(matches, types)

    def _ObtainREString(self, types):
        re_string = ''
        for attribute_type in types:
            re_string += '(?:/' + attribute_type.AttributesString()\
                + '/(?P<' + attribute_type.AttributesString() + \
                '>(?:\d+,)*\d+))?'
        return re_string

    def _ProcessMatches(self, matches, types):
        if matches == None:
            raise Http404

        for attribute_type in types:
            self._string_processors.append(
                CSVStringProcessor(
                    attribute_type.AttributesString(),
                    attribute_type,
                    matches.group(attribute_type.AttributesString())
                    ))

class UrlBasedSignFilter:
    def __init__(self,
                 filter_string):
        self.string_processor = FilterStringProcessor(
            filter_string,
            [BodyLocation, Tag, Gloss])

        self._multi_filter = MultiFilter()

        self._AddFilters(self.string_processor.ObtainAttributes())

    def ObtainFilteredSigns(self):
        filtered_signs = self._multi_filter.FilterSigns(
            list(Sign.objects.all()))

        return filtered_signs

    def InFilter(self, attribute):
        return self.string_processor.InList(attribute)

    def ObtainToggleFilterString(self, attribute):
       return self.string_processor.ObtainToggleFilterString(attribute)

    def _AddFilters(self, attributes):

        for attribute in attributes:
            self._multi_filter.AddFilter(attribute)
