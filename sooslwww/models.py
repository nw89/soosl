from django.db import models

# Create your models here.

class WrittenLanguage(models.Model):
    def __unicode__(self):
        return self.name

    name = models.TextField()

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

class Sign(models.Model):
    def __unicode__(self):
        return self.videohash

    videohash = models.CharField(max_length = 40)
    deleted = models.BooleanField(False)

    tags = models.ManyToManyField(Tag);


class Gloss(models.Model):
    def __unicode__(self):
        return self.text

    language = models.ForeignKey(WrittenLanguage)
    text = models.TextField()
