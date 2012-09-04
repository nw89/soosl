from django.http import HttpResponse

def generateFileHttpResponse(filePath, mimeType):
    file = open(filePath, 'rb');

    # Todo: this will never suffice for production - we're essentially
    # copying the file into memory and rewriting it to the browser
    response = HttpResponse(mimetype = mimeType)
    response.write(file.read())
    return response
