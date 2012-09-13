from django.http import HttpResponse

from sooslwww.models import Gloss

def StripLastComma(string):
    if string == '':
        return string
    if string[-1] == ',':
        return string[:-1]
    else:
        return string

def generateFileHttpResponse(filePath, mimeType):
    file = open(filePath, 'rb');

    # Todo: this will never suffice for production - we're essentially
    # copying the file into memory and rewriting it to the browser
    response = HttpResponse(mimetype = mimeType)
    response.write(file.read())
    return response

def AddNewGloss(sign, language_id, gloss_text):
    #Check too see if there are any similar glosses
    #TODO: language
    glosses = Gloss.objects.filter(
        text__exact=gloss_text,
        language__id__exact=language_id)

    if glosses.exists():
        gloss = glosses[0]
    else:
        gloss = Gloss(language_id = language_id, text = gloss_text)
        gloss.save()

    sign.glosses.add(gloss)
