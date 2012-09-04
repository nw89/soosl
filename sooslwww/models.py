from django.db import models

# Create your models here.

class WrittenLanguage(models.Model):
    def __unicode__(self):
        return self.name

    name = models.TextField()

class Sign(models.Model):
    def __unicode__(self):
        return self.videopath;

    videopath = models.FileField(upload_to="videos/")
    deleted = models.BooleanField(False)

class Gloss(models.Model):
    def __unicode__(self):
        return self.text;

    language = models.ForeignKey(WrittenLanguage)
    text = models.TextField()
