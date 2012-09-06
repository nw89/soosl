from django.contrib import admin
from  sooslwww.models import Dialect, Gloss, WrittenLanguage, Sign, TagType, Tag

admin.site.register(WrittenLanguage)

admin.site.register(Sign)

admin.site.register(TagType)
admin.site.register(Tag)

admin.site.register(Gloss)
admin.site.register(Dialect)
