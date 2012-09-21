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

    @staticmethod
    def AttributesString():
        return 'tags'

    type = models.ForeignKey(TagType)
    text = models.TextField(max_length = 128)
    graphic = models.FileField(upload_to='tags')

class WrittenLanguage(models.Model):
    def __unicode__(self):
        return self.name

    name = models.TextField()

# class Dialect(models.Model):
#     def __unicode____(self):
#         return self.name

#     language = models.ForeignKey(WrittenLanguage)
#     name = models.TextField()


class TextWithLanguage(models.Model):
    def __unicode__(self):
        return self.text

    language = models.ForeignKey(WrittenLanguage)

    class Meta:
        abstract = True

class Gloss(TextWithLanguage):
    text = models.TextField(max_length = 128)

    @staticmethod
    def AttributesString():
        return 'glosses'

class SentenceGloss(TextWithLanguage):
    text = models.TextField(max_length = 1024)
    glosses = models.ManyToManyField(
        Gloss,
        through='SentenceGlossRelationship')

class SentenceGlossRelationship(models.Model):
    gloss = models.ForeignKey(Gloss)
    sentenceGloss = models.ForeignKey(SentenceGloss)
    wordNumber=models.IntegerField()

class BodyHeadLocationType(models.Model):
    text=models.CharField(max_length=64)
    color=models.CharField(max_length=32)
    hover_color=models.CharField(max_length=32)

class BodyLocation(models.Model):
    @staticmethod
    def AttributesString():
        return 'body_locations'

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

    #The following fields allow the subclass to be obtained from this (parent class)
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

class Video (models.Model):
    def __unicode__(self):
        return self.videohash

    videohash = models.CharField(max_length = 40)
    deleted = models.BooleanField(False)

    @staticmethod
    def GetByHash(video_hash):
        return (Video.objects.get(videohash=video_hash).\
                get_instance())

    @staticmethod
    def UploadedAlready(video_hash):
        return (Video.objects.filter(videohash=video_hash).exists())

    #The following fields allow the subclass to be obtained from this (parent class)
    video_type = models.ForeignKey(ContentType,editable=False)

    def save(self,force_insert=False,force_update=False):
        if self.video_type_id is None:
            self.video_type = ContentType.objects.get_for_model(self.__class__)
            super(Video,self).save(force_insert,force_update)

    def get_instance(self):
        return self.video_type.get_object_for_this_type(id=self.id)

class Sign(Video):
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

        elif tag.__class__ == Tag:
            return (self.tags.filter(id__exact=tag.id).exists())
        else:
            raise NotImplementedError()

    def HasGloss(self, gloss):
        if type(gloss) == unicode:
            return (self.glosses.filter(id__exact=int(gloss)).exists())
        if type(gloss) == int:
            return (self.glosses.filter(id__exact=gloss).exists())
        elif gloss.__class__ == Gloss:
            return (self.glosses.filter(id__exact=gloss.id).exists())
        else:
            raise NotImplementedError

    def HasBodyLocation(self, location):
        if type(location) == unicode:
            return (self.body_locations.filter(id__exact=int(location)).exists())
        if type(location) == int:
            return (self.body_locations.filter(id__exact=location).exists())
        elif location.__class__ == BodyLocation:
            return (self.body_locations.filter(id__exact=location.id).exists())
        else:
            raise NotImplementedError

    def HasAttribute(self, attribute):
        if attribute.__class__ == BodyLocation:
            return self.HasBodyLocation(attribute)
        elif attribute.__class__ == Gloss:
            return self.HasGloss(attribute)
        elif attribute.__class__ == Tag:
            return self.HasTag(attribute)
        else:
            raise NotImplementedError

    def HasAHeadLocation(self):
        return(self.body_locations.filter(
            id=BodyLocation.GetHead().id).exists())

    def _RemoveHeadLocations(self):
        head_locations = BodyLocation.objects.filter(on_head=True)

        for location in head_locations:
            self.RemoveBodyLocation(location)

    def AddBodyLocation(self, location):
        self.body_locations.add(location)

        if location.on_head:
            self.AddBodyLocation(BodyLocation.GetHead())

    def RemoveBodyLocation(self, location):
        self.body_locations.remove(location)

        if location.IsHead():
            self._RemoveHeadLocations()

    def GlossesForLanguage(self, language_id):
        return (self.glosses.filter(
            language__id=language_id))

    def GetSentences(self):
        return Sentence.objects.filter(signs__id__exact=self.id)

class Sentence(Video):
    signs = models.ManyToManyField(Sign, blank=True, null=True)
    glosses = models.ManyToManyField(SentenceGloss,
                                     blank=True,
                                     null=True)

    def GetSigns(self):
        return self.signs.all()

    def AddSign(self, sign):
        self.signs.add(sign)

    def RemoveSign(self, sign):
        self.signs.remove(sign)
