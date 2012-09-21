from sooslwww.controllers.Controller import AbstractController, RedirectingException
from sooslwww.forms import AddSignForm
from sooslwww.models import Video, Sign, Sentence
from sooslwww.videoHandler import VideoUploadHandler, BadVideo
from sooslwww.urlresolver import ViewVideoUrl

class AddVideoController(AbstractController):
    def __init__(self):
        AbstractController.__init__(self)
        self._form = AddSignForm()

    def _PreprocessRequest(self, request):
        if request.method == 'POST':
            self._form = AddSignForm(request.POST, request.FILES)

            if self._form.is_valid():
                    self.__ProcessVideo(request.FILES['videoFile'])

        self._AddToDictionary('form', self._form)

    def __ProcessVideo(self, uploaded_video):
        videoHandler = VideoUploadHandler(uploaded_video)

        if Video.UploadedAlready(videoHandler.hash()):
            raise RedirectingException(
                ViewVideoUrl(Video.GetByHash(videoHandler.hash())))

        else:
            try:
                videoHandler.encodeVideo()
            except BadVideo:
                errors = self._form._errors.setdefault(
                "videoFile", ErrorList())
                errors.append("That video could not be converted.")

            new_video = self._AttributeType()(videohash=\
                                              videoHandler.hash())

            new_video.save()

            raise RedirectingException(ViewVideoUrl(new_video))

    def _AttributeType(self):
        raise NotImplementedError

    def _View(self):
        raise NotImplementedError

class AddSignController(AddVideoController):
    def __init__(self):
        AddVideoController.__init__(self)

    def _AttributeType(self):
        return Sign

    def _View(self):
        return 'sooslwww.view.add_sign'

    def _TemplateFile(self):
        return 'addsign.html'


class AddSentenceController(AddVideoController):
    def __init__(self):
        AddVideoController.__init__(self)

    def _AttributeType(self):
        return Sentence

    def _View(self):
        return 'sooslwww.view.add_sentence'

    def _TemplateFile(self):
        return 'addsentence.html'
