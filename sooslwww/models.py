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
