import string

from django.db import models

# Create your models here.

class TagType(models.Model):
    def __unicode__(self):
	return self.text

    text = models.TextField(max_length = 128)


class Tag(models.Model):
    def __unicode__(self):
	return self.graphic.name

    type = models.ForeignKey(TagType)
    text = models.TextField(max_length = 128)
    graphic = models.FileField(upload_to='tags')

class WrittenLanguage(models.Model):
    def __unicode__(self):
	return self.name

    name = models.TextField()

class Dialect(models.Model):
    def __unicode____(self):
	return self.name

    language = models.ForeignKey(WrittenLanguage)
    name = models.TextField()


class Gloss(models.Model):
    def __unicode__(self):
	return self.text

    language = models.ForeignKey(WrittenLanguage)
    text = models.TextField(max_length = 128)

    dialects = models.ManyToManyField(Dialect, blank=True, null=True)

class Sign(models.Model):
    def __unicode__(self):
	return self.videohash

    videohash = models.CharField(max_length = 40)
    deleted = models.BooleanField(False)

    tags = models.ManyToManyField(Tag, blank=True, null=True);
    glosses = models.ManyToManyField(Gloss, blank=True, null=True)

    def HasTag(self, tag):
	if type(tag) == unicode:
	    return (self.tags.filter(id__exact=int(tag)).exists())
	elif type(tag) == int:
	    return (self.tags.filter(id__exact=tag).exists())

	elif type(tag) == Tag:
	    return (self.tags.filter(id__exact=tag.id).exists())
	else:
	    raise NotImplementedError()

    def HasGloass(self, gloss):
	if type(gloss) == unicode:
	    return (self.glosses.filter(id__exact=int(gloss)).exists())
	if type(gloss) == int:
	    return (self.glosses.filter(id__exact=gloss).exists())
	elif type(gloss) == Gloss:
	    return (self.glosses.filter(id__exact=gloss.id).exists())
	else:
	    raise NotImplementedError()
