from django.contrib import admin
from  sooslwww.models import Gloss, WrittenLanguage, Sign, TagType, Tag

admin.site.register(WrittenLanguage)

admin.site.register(Sign)

admin.site.register(TagType)
admin.site.register(Tag)

admin.site.register(Gloss)
