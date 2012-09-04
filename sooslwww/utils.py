# Copyright (c) 2010, Andre Engelbrecht
# All rights reserved.

# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

#     * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#     * Neither the name of django-video nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#Taken from https://github.com/andrewebdev/django-video/blob/master/src/videostream/utils.py


import commands
import os

from django.conf import settings


# This allows the developer to override the binary path for ffmpeg
FFMPEG_BINARY_PATH = getattr(settings, 'FFMPEG_BINARY_PATH', 'ffmpeg')
FLVTOOL_PATH = getattr(settings, 'FLVTOOL_PATH', 'flvtool2')


def encode_video(video):
    MEDIA_ROOT = getattr(settings, 'MEDIA_ROOT')
    VIDEOSTREAM_SIZE = getattr(settings, 'VIDEOSTREAM_SIZE', '320x240')
    VIDEOSTREAM_THUMBNAIL_SIZE = getattr(settings,
        'VIDEOSTREAM_THUMBNAIL_SIZE', '320x240')

    flvfilename = "test.flv" #  % flashvideo.slug
    infile = "%s/videos/%s" % (MEDIA_ROOT, video)
    outfile = "%s/videos/flv/%s" % (MEDIA_ROOT, flvfilename)
    thumbnailfilename = "%s/videos/thumbnails/%s.gif" % (
        MEDIA_ROOT, "test")

    # Final Results
    flvurl = "videos/flv/%s" % flvfilename
    thumburl = "videos/thumbnails/%s.png" % "test"

    # Check if flv and thumbnail folder exists and create if not
    if not(os.access("%s/videos/flv/" % MEDIA_ROOT, os.F_OK)):
        os.makedirs("%s/videos/flv" % MEDIA_ROOT)

    if not(os.access("%s/videos/thumbnails/" % MEDIA_ROOT, os.F_OK)):
        os.makedirs("%s/videos/thumbnails" % MEDIA_ROOT)

    # ffmpeg command to create flv video
    ffmpeg = "%s -y -i %s -acodec libmp3lame -ar 22050 -ab 32000 -f flv -s %s %s" % (
        FFMPEG_BINARY_PATH, infile, VIDEOSTREAM_SIZE, outfile)

    # ffmpeg command to create the video thumbnail
    #getThumb = "%s -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s %s %s" % (
    #    FFMPEG_BINARY_PATH, infile, VIDEOSTREAM_THUMBNAIL_SIZE, thumbnailfilename)

    #getThumb = "%s -y -i %s -pix_fmt rgb24 -vf \"select='not(mod(n,10))'\" -s 64x48  %s" % (
    #   FFMPEG_BINARY_PATH, infile, thumbnailfilename)
    getThumb = "mplayer  %s -ao null -vo gif89a:fps=2:output=%s- -vf scale=64:48" % (
        infile, thumbnailfilename)



    #getThumb = "%s -y -i %s -vframes 10 -s %s  -skip_factor 10 %s" % (
    #     FFMPEG_BINARY_PATH, infile, VIDEOSTREAM_THUMBNAIL_SIZE, thumbnailfilename)

    # flvtool command to get the metadata
    flvtool = "%s -U %s" % (FLVTOOL_PATH, outfile)

    # Lets do the conversion
    ffmpegresult = commands.getoutput(ffmpeg)
    print 80*"~"
    print ffmpegresult

    if os.access(outfile, os.F_OK): # outfile exists

        # There was a error cause the outfile size is zero
        if (os.stat(outfile).st_size==0):
            # We remove the file so that it does not cause confusion
            os.remove(outfile)

        else:
            # there does not seem to be errors, follow the rest of the procedures
            flvtoolresult = commands.getoutput(flvtool)
            print flvtoolresult

            thumbresult = commands.getoutput(getThumb)
            print thumbresult

    print 80*"~"


# def encode_video_set(queryset=None):

#     if not queryset:
#         queryset = FlashVideo.objects.filter(encode=True)

#     for flashvideo in queryset:
#         encode_video(flashvideo)
