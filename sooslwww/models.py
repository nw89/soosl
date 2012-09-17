import string

from django.contrib.contenttypes.models import ContentType
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

class BodyHeadLocationType(models.Model):
    text=models.CharField(max_length=64)
    color=models.CharField(max_length=32)
    hover_color=models.CharField(max_length=32)

class BodyLocation(models.Model):
    text=models.CharField(max_length=128)
    type=models.ForeignKey(BodyHeadLocationType)
    behind=models.BooleanField(False)
    on_head=models.BooleanField(False)

    HEAD_ID = 0

    def Shape_str(self):
        raise NotImplementedError

    def IsHead(self):
        return (self.id == BodyLocation.HEAD_ID)

    @staticmethod
    def GetHead():
        return (BodyLocation.objects.get(
                id=BodyLocation.HEAD_ID))

    #The following fields allow the subclass to be obtained from this (paretn class)
    shape = models.ForeignKey(ContentType,editable=False)

    def save(self,force_insert=False,force_update=False):
        if self.shape_id is None:
            self.shape = ContentType.objects.get_for_model(self.__class__)
            super(BodyLocation,self).save(force_insert,force_update)

    def get_instance(self):
        return self.shape.get_object_for_this_type(id=self.id)


class BodyLocationCircle(BodyLocation):
    def Shape_str(self):
        return 'circle'

    radius=models.DecimalField(max_digits=5,decimal_places=2)
    center_x=models.DecimalField(max_digits=5,decimal_places=2)
    center_y=models.DecimalField(max_digits=5,decimal_places=2)

class BodyLocationEllipse(BodyLocation):
    def Shape_str(self):
        return 'ellipse'

    radius_x=models.DecimalField(max_digits=5,decimal_places=2)
    radius_y=models.DecimalField(max_digits=5,decimal_places=2)
    center_x=models.DecimalField(max_digits=5,decimal_places=2)
    center_y=models.DecimalField(max_digits=5,decimal_places=2)

class BodyLocationRectangle(BodyLocation):
    def Shape_str(self):
        return 'rect'

    x=models.DecimalField(max_digits=5,decimal_places=2)
    y=models.DecimalField(max_digits=5,decimal_places=2)
    width=models.DecimalField(max_digits=5,decimal_places=2)
    height=models.DecimalField(max_digits=5,decimal_places=2)

class BodyLocationPolygon(BodyLocation):
        def Shape_str(self):
            return 'polygon'

        def Points(self):
            return self.points.all()

class BodyLocationPolygonPoint(models.Model):
    polygon=models.ForeignKey(BodyLocationPolygon,
                              related_name='points')
    x=models.DecimalField(max_digits=5,decimal_places=2)
    y=models.DecimalField(max_digits=5,decimal_places=2)

class Sign(models.Model):
    def __unicode__(self):
        return self.videohash

    videohash = models.CharField(max_length = 40)
    deleted = models.BooleanField(False)

    tags = models.ManyToManyField(Tag, blank=True, null=True);
    glosses = models.ManyToManyField(Gloss, blank=True, null=True)
    body_locations = models.ManyToManyField(BodyLocation,
                                            blank=True,
                                            null=True)

    def HasTag(self, tag):
        if type(tag) == unicode:
            return (self.tags.filter(id__exact=int(tag)).exists())
        elif type(tag) == int:
            return (self.tags.filter(id__exact=tag).exists())

        elif type(tag) == Tag:
            return (self.tags.filter(id__exact=tag.id).exists())
        else:
            raise NotImplementedError()

    def HasGloss(self, gloss):
        if type(gloss) == unicode:
            return (self.glosses.filter(id__exact=int(gloss)).exists())
        if type(gloss) == int:
            return (self.glosses.filter(id__exact=gloss).exists())
        elif type(gloss) == Gloss:
            return (self.glosses.filter(id__exact=gloss.id).exists())
        else:
            raise NotImplementedError()

    def HasBodyLocation(self, location):
        if type(location) == unicode:
            return (self.body_locations.filter(id__exact=int(location)).exists())
        if type(location) == int:
            return (self.body_locations.filter(id__exact=location).exists())
        elif type(location) == BodyLocation:
            return (self.body_locations.filter(id__exact=location.id).exists())
        else:
            raise NotImplementedError()

    def HasAHeadLocation(self):
        return(self.body_locations.filter(
                id=BodyLocation.GetHead().id).exists())

    def RemoveBodyLocation(self, location):
        self.body_locations.remove(location)

        if location.IsHead():
            self._RemoveHeadLocations()


    def _RemoveHeadLocations(self):
        head_locations = BodyLocation.objects.filter(on_head=True)

        for location in head_locations:
            self.RemoveBodyLocation(location)

    def AddBodyLocation(self, location):
        self.body_locations.add(location)

        if location.on_head:
            self.AddBodyLocation(BodyLocation.GetHead())
