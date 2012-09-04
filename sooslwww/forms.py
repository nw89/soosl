# -*- coding: utf-8 -*-
from django import forms

class AddSignForm(forms.Form):
    videoFile = forms.FileField(
        label='Please choose a video file to upload.'
    )
