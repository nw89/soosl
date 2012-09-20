from sooslwww.models import BodyLocation, Tag, Gloss

class Filter:
    def SignMatches(self, sign):
        '''Indicates whether the sign matches (passes through) \
        the filter'''
        raise NotImplementedError()

    def FilterSigns(self, signs):
        filtered_signs = [sign for sign in signs \
                              if self.SignMatches(sign)]
        return filtered_signs

class TagFilter(Filter):
    def  __init__(self, tag):
        self._tag = tag

    def SignMatches(self, sign):
        return (sign.HasTag(self._tag))

class GlossFilter(Filter):
    def __init__(self, gloss):
        self._gloss = gloss

    def SignMatches(self, sign):
        return (sign.HasGloss(self._gloss))

class BodyLocationFilter(Filter):
    def __init__(self, body_location):
        self._body_location = body_location

    def SignMatches(self, sign):
        return (sign.HasBodyLocation(self._body_location))


def ObtainFilter(attribute):
    if attribute.__class__ == Tag:
        return TagFilter(attribute)

    elif attribute.__class__ == Gloss:
        return GlossFilter(attribute)

    elif attribute.__class__ == BodyLocation:
        return BodyLocationFilter(attribute)

    else:
        raise NotImplementedError()

class MultiFilter:
    def __init__(self):
        self._filters = []

    def AddFilter(self, attribute):
        self._filters.append(ObtainFilter(attribute))

    def FilterSigns(self, signs):
        for filter in self._filters:
            signs = filter.FilterSigns(signs)
        return signs
