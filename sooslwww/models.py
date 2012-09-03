from django.db import models

# Create your models here.

class WrittenLanguage(models.Model):
    def __unicode__(self):
        return self.name

    name = models.TextField()

class Sign(models.Model):
    def __unicode__(self):
        return self.videopath;

    videopath = models.CharField(max_length=256)
    deleted = models.BooleanField()

class Gloss(models.Model):
    def __unicode__(self):
        return self.text;

    language = models.ForeignKey(WrittenLanguage)
    text = models.TextField()
