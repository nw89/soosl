import commands
import glob
import hashlib
import os

from django.conf import settings

class VideoUploadHandler():
    def __init__(self, uploadedFile):
        self._workingFileName = getattr(settings, 'MEDIA_ROOT') + "/videos/tmp/" + uploadedFile.name

        #TODO check for valid file extensions

        with open(self._workingFileName, 'wb') as workingFile:

            for chunk in uploadedFile.chunks():
                workingFile.write(chunk)

        #File is now stored, generate hash
        with open(self._workingFileName, 'rb') as workingFile:
            hasher = hashlib.sha1()
            hasher.update(workingFile.read())

            self._hash = hasher.hexdigest()


    def __del__(self):
        #delete everything in tmp
        files = glob.glob(getattr(settings, 'MEDIA_ROOT') + "/videos/tmp/*")
        for file in files:
            os.remove(file)

    def obtainFilePath(self, type):
        if type == "mp4":
            folder = "mp4"
            ending = ".mp4"

        elif type == "thumbnail":
            folder = "thumbnails"
            ending = ".gif"

        elif type == "capturedframesffmpeg":
            folder = "tmp"
            ending = "_%05d.jpg"

        elif type == "capturedframesconvert":
            folder = "tmp"
            ending = "_*.jpg"
        else:
            assert False

        filePath = "%s/videos/%s/%s%s" % (
            getattr(settings, 'MEDIA_ROOT'), folder, self.hash(), ending)
        return filePath

    def hash(self):
        return self._hash

    def encodeVideo(self):
        success = self.generateMP4()
        if not success:
            return False

        success = self.generateThumbnail()
        if not success:
            return False

        return True


    def generateMP4(self):
        createMP4Command = "ffmpeg -y -i %s -an -vcodec libx264 -f mp4 -s %sx%s %s" % (
            self._workingFileName,
            getattr(settings, 'VIDEO')['width'],
            getattr(settings, 'VIDEO')['height'],
            self.obtainFilePath("mp4"))

        statusoutput = commands.getstatusoutput(createMP4Command)

        #Print output
        print 80*"~"
        print statusoutput[1]

        #Return whether successful
        return (statusoutput[0] == 0)

    def generateThumbnail(self):
        createThumbnailsCommand1 = "ffmpeg -y -i %s -an -r 3 -s 128x96 %s" % (
            self.obtainFilePath("mp4"),
            self.obtainFilePath("capturedframesffmpeg"))

        statusoutput = commands.getstatusoutput(createThumbnailsCommand1)

        #Print output
        print 80*"~"
        print "Status: " + str(statusoutput[0])
        print statusoutput[1]

        #Stop if unsuccessful
        if statusoutput[0] != 0:
            return False

        createThumbnailsCommand2 = "convert -delay 33 -loop 0 %s %s" % (
            self.obtainFilePath("capturedframesconvert"),
            self.obtainFilePath("thumbnail"))

        statusoutput = commands.getstatusoutput(createThumbnailsCommand2)
        print 80*"~"
        print "Status: " + str(statusoutput[0])
        print statusoutput[1]


        #Return whether successful
        return (statusoutput[0] == 0)
