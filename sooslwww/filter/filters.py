from sooslwww.models import Tag, Gloss

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

def ObtainFilter(attribute):
    if type(attribute) == Tag:
	return TagFilter(attribute)

    elif type(attribute) == Gloss:
	return GlossFilter(attribute)

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
